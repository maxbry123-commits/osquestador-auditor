/**
 * Heritrix Groovy (Spring beans DSL) language support for CodeMirror.
 *
 * Exports a single factory function `heritrixGroovy(beandoc)` that returns a
 * CodeMirror extension array with Groovy syntax highlighting and Heritrix-aware
 * autocomplete.
 *
 * Autocomplete contexts:
 *  1. import statements:  "import org.archive." -> suggests matching FQNs from beandoc
 *  2. Bean class argument:  "fetchHttp(|)" -> suggests class short names, auto-inserts import
 *  3. Property names inside a bean closure:  "fetchHttp(FetchHTTP) {\n  maxLen|" ->
 *     suggests property names for the resolved bean class
 *  4. ref() argument:  "ref('|')" -> suggests bean ids declared in the document
 *  5. new ClassName:  "new Reject|" -> suggests class names, auto-inserts import
 *  6. new ClassName named args (single or multi-line):
 *       "new TooManyHopsDecideRule(\n        maxHops|" ->
 *     suggests property names for the class, applied with trailing ": "
 *
 * After editing this file, run:
 *   node engine/src/test/js/heritrix-groovy-test.js
 */

import {StreamLanguage, indentUnit} from "@codemirror/language"
import {EditorView} from "@codemirror/view"
import {startCompletion} from "@codemirror/autocomplete"
import {groovy} from "@codemirror/legacy-modes/mode/groovy.js"

/**
 * Map of fully-qualified bean class names to their definitions.
 * @typedef {Object<string, Bean>} BeanDoc
 */

/**
 * One bean entry describing the bean and its properties.
 * @typedef {Object} Bean
 * @property {string} description
 * @property {Object<string, Property>} properties - Map of property name to metadata.
 */

/**
 * Metadata for a single property on a bean.
 * @typedef {Object} Property
 * @property {string} description
 * @property {string} type - The Java type
 * @property {*} [default] - Optional default value; may be number, boolean, string, etc.
 */

/**
 * Strips the package from a fully qualified class name (including generic types).
 * @param {string} className e.g. "java.util.List<java.lang.String>"
 * @returns {string} e.g. "List<String>"
 */
function stripPackage(className) {
    return className.replace(/\b[^<>, ]+\./g, "");
}

function makeDiv(html) {
    if (!html) return null;
    const div = document.createElement('div');
    div.innerHTML = html.replace(/\n\n/g, "<br><br>").replace(/\n/g, " ");
    return div;
}

/**
 * Parse the import statements in the document text and return a map from
 * short name (or wildcard package prefix) to fully-qualified name / package.
 *
 * @param {string} docText
 * @returns {{ exact: Map<string,string>, wildcards: string[] }}
 *   exact: short class name -> fqn
 *   wildcards: array of package prefixes (e.g. "org.archive.modules")
 */
function parseImports(docText) {
    const exact = new Map();
    const wildcards = [];
    for (const match of docText.matchAll(/^import\s+([\w.]+(?:\.\*)?)\s*$/gm)) {
        const imp = match[1];
        if (imp.endsWith('.*')) {
            wildcards.push(imp.slice(0, -2)); // strip trailing .*
        } else {
            const short = imp.replace(/.*\./, '');
            exact.set(short, imp);
        }
    }
    return {exact, wildcards};
}

/**
 * Given a short or partial class name, resolve matching fully-qualified class names
 * from beandoc.
 *
 * @param {string} partial  The text typed so far (may be short name or partial fqn)
 * @param {BeanDoc} beandoc
 * @returns {string[]} Matching fully-qualified class names
 */
function resolveClassMatches(partial, beandoc) {
    const lower = partial.toLowerCase();
    return Object.keys(beandoc).filter(fqn => {
        const short = fqn.replace(/.*\./, '');
        if (!partial) return true;
        return fqn.toLowerCase().includes(lower) || short.toLowerCase().includes(lower);
    });
}

/**
 * Resolve a short or fully-qualified class name to a fully-qualified beandoc key.
 *
 * @param {string} nameInCode
 * @param {{ exact: Map<string,string>, wildcards: string[] }} imports
 * @param {BeanDoc} beandoc
 * @returns {string|null}
 */
function resolveClassName(nameInCode, imports, beandoc) {
    if (nameInCode.includes('.')) return beandoc[nameInCode] ? nameInCode : null;

    if (imports.exact.has(nameInCode)) {
        const fqn = imports.exact.get(nameInCode);
        return beandoc[fqn] ? fqn : null;
    }

    for (const pkg of imports.wildcards) {
        const candidate = pkg + '.' + nameInCode;
        if (beandoc[candidate]) return candidate;
    }

    for (const fqn of Object.keys(beandoc)) {
        if (fqn.replace(/.*\./, '') === nameInCode) return fqn;
    }

    return null;
}

/**
 * Find the character position after the last import statement (or after the leading
 * block comment if there are no imports yet), for inserting a new import line.
 *
 * @param {string} docText
 * @returns {number}
 */
function findImportInsertPosition(docText) {
    const lines = docText.split('\n');
    let lastImportEnd = -1;
    let afterLeadingComments = 0;
    let inBlockComment = false;
    let offset = 0;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();

        if (inBlockComment) {
            offset += line.length + 1;
            if (trimmed.includes('*/')) {
                inBlockComment = false;
                afterLeadingComments = offset;
            }
            continue;
        }

        if (trimmed.startsWith('/*')) {
            inBlockComment = true;
            offset += line.length + 1;
            if (trimmed.includes('*/')) {
                inBlockComment = false;
                afterLeadingComments = offset;
            }
            continue;
        }

        if (trimmed.startsWith('//') || trimmed === '') {
            offset += line.length + 1;
            if (trimmed === '' && lastImportEnd === -1) afterLeadingComments = offset;
            continue;
        }

        if (trimmed.startsWith('import ')) {
            lastImportEnd = offset + line.length + 1;
        }

        offset += line.length + 1;
    }

    return lastImportEnd >= 0 ? lastImportEnd : afterLeadingComments;
}

/**
 * Returns a CodeMirror transaction spec that inserts an import statement for the
 * given fully-qualified class name if it is not already imported.
 * Returns null if no insertion is needed.
 *
 * @param {import("@codemirror/state").EditorState} state
 * @param {string} fqn  Fully-qualified class name to import
 * @returns {import("@codemirror/state").TransactionSpec | null}
 */
function importInsertTransaction(state, fqn) {
    const docText = state.doc.toString();
    const pkg = fqn.replace(/\.[^.]+$/, '');
    const alreadyExact = new RegExp('^import\\s+' + fqn.replace(/\./g, '\\.') + '\\s*$', 'm').test(docText);
    const alreadyWild = new RegExp('^import\\s+' + pkg.replace(/\./g, '\\.') + '\\.\\*\\s*$', 'm').test(docText);
    if (alreadyExact || alreadyWild) return null;

    return {changes: {from: findImportInsertPosition(docText), insert: 'import ' + fqn + '\n'}};
}

const MATCHING_OPEN = {')': '(', ']': '[', '}': '{'};

function canStartSlashyString(previous) {
    return !previous || "([{,:;=!?&|+-*~".includes(previous);
}

/**
 * Lex just enough Groovy to know whether `pos` is in code, a string/comment,
 * and which brackets are open.
 *
 * @param {string} docText
 * @param {number} pos
 * @returns {{
 *   stack: {ch: string, pos: number, lineStart: number}[],
 *   inString: boolean,
 *   stringQuote: string|null,
 *   stringStart: number,
 *   stringTriple: boolean,
 *   inComment: boolean,
 *   lastCode: string
 * }}
 */
function scanGroovyContext(docText, pos) {
    const stack = [];
    let mode = "code";
    let quote = null;
    let stringStart = -1;
    let triple = false;
    let lineStart = 0;
    let lastCode = '';

    for (let i = 0; i < pos;) {
        const ch = docText[i];
        const next = docText[i + 1];

        if (mode === "lineComment") {
            if (ch === '\n') {
                mode = "code";
                lineStart = i + 1;
            }
            i++;
            continue;
        }

        if (mode === "blockComment") {
            if (ch === '*' && next === '/') {
                mode = "code";
                i += 2;
                continue;
            }
            if (ch === '\n') lineStart = i + 1;
            i++;
            continue;
        }

        if (mode === "string") {
            if (triple) {
                if (ch === quote && next === quote && docText[i + 2] === quote) {
                    mode = "code";
                    quote = null;
                    triple = false;
                    stringStart = -1;
                    i += 3;
                    continue;
                }
                if (ch === '\n') lineStart = i + 1;
                i++;
                continue;
            }

            if (ch === '\\') {
                i += 2;
                continue;
            }
            if (ch === quote) {
                mode = "code";
                quote = null;
                stringStart = -1;
                i++;
                continue;
            }
            // Recover from unfinished single-line strings so one bad quote does
            // not disable completion for the rest of the file.
            if (ch === '\n') {
                mode = "code";
                quote = null;
                stringStart = -1;
                lineStart = i + 1;
            }
            i++;
            continue;
        }

        if (mode === "slashyString") {
            if (ch === '\\') {
                i += 2;
                continue;
            }
            if (ch === '/') {
                mode = "code";
                quote = null;
                stringStart = -1;
                i++;
                continue;
            }
            if (ch === '\n') lineStart = i + 1;
            i++;
            continue;
        }

        if (mode === "dollarSlashyString") {
            if (ch === '/' && next === '$') {
                mode = "code";
                quote = null;
                stringStart = -1;
                i += 2;
                continue;
            }
            if (ch === '$') {
                i += 2;
                continue;
            }
            if (ch === '\n') lineStart = i + 1;
            i++;
            continue;
        }

        if (ch === '\n') {
            lineStart = i + 1;
            i++;
            continue;
        }
        if (ch === '/' && next === '/') {
            mode = "lineComment";
            i += 2;
            continue;
        }
        if (ch === '/' && next === '*') {
            mode = "blockComment";
            i += 2;
            continue;
        }
        if (ch === '$' && next === '/' && canStartSlashyString(lastCode)) {
            mode = "dollarSlashyString";
            quote = '$/';
            stringStart = i;
            i += 2;
            continue;
        }
        if (ch === '/' && canStartSlashyString(lastCode)) {
            mode = "slashyString";
            quote = '/';
            stringStart = i;
            i++;
            continue;
        }
        if (ch === "'" || ch === '"') {
            mode = "string";
            quote = ch;
            stringStart = i;
            triple = next === ch && docText[i + 2] === ch;
            i += triple ? 3 : 1;
            continue;
        }
        if (ch === '(' || ch === '[' || ch === '{') {
            stack.push({ch, pos: i, lineStart});
            lastCode = ch;
            i++;
            continue;
        }
        if (ch === ')' || ch === ']' || ch === '}') {
            const open = MATCHING_OPEN[ch];
            for (let j = stack.length - 1; j >= 0; j--) {
                if (stack[j].ch === open) {
                    stack.splice(j);
                    break;
                }
            }
            lastCode = ch;
            i++;
            continue;
        }
        if (!/\s/.test(ch)) lastCode = ch;
        i++;
    }

    return {
        stack,
        inString: mode === "string" || mode === "slashyString" || mode === "dollarSlashyString",
        stringQuote: quote,
        stringStart,
        stringTriple: triple,
        inComment: mode === "lineComment" || mode === "blockComment",
        lastCode,
    };
}

/**
 * Return the previous non-whitespace character that is real code, ignoring
 * strings and comments.
 *
 * @param {string} docText
 * @param {number} pos
 * @returns {string}
 */
function previousCodeChar(docText, pos) {
    return scanGroovyContext(docText, pos).lastCode;
}

function topFrame(context) {
    return context.stack[context.stack.length - 1] || null;
}

/**
 * Return the direct enclosing Groovy Spring bean DSL bean definition, i.e.
 * the innermost open brace at `pos` must come from a line matching:
 *   beanId(ClassName) {
 * or
 *   beanId(ClassName) { bean ->
 *
 * Returns the fully-qualified class name, or null if not found.
 * @param {string} docText
 * @param {ReturnType<typeof scanGroovyContext>} context
 * @param {{ exact: Map<string,string>, wildcards: string[] }} imports
 * @param {BeanDoc} beandoc
 * @returns {string|null}
 */
function findEnclosingBeanClassInContext(docText, context, imports, beandoc) {
    if (context.inString || context.inComment) return null;

    const frame = topFrame(context);
    if (!frame || frame.ch !== '{') return null;

    const line = docText.slice(frame.lineStart, frame.pos).trim();
    const m = line.match(/^\w+\s*\(\s*([\w.]+)\s*\)$/);
    if (!m) return null;

    return resolveClassName(m[1], imports, beandoc);
}

/**
 * @param {string} docText
 * @param {{ch: string, pos: number, lineStart: number}} frame
 * @returns {boolean}
 */
function isBeansBlockFrame(docText, frame) {
    return frame.ch === '{' && docText.slice(frame.lineStart, frame.pos).trim() === 'beans';
}

/**
 * Scan the document for direct children of the top-level beans block:
 *   beanId(ClassName) { ... }
 * or
 *   beanId(ClassName)
 * and return an array of {id, fqn} objects.
 *
 * @param {string} docText
 * @param {{ exact: Map<string,string>, wildcards: string[] }} imports
 * @param {BeanDoc} beandoc
 * @returns {{id: string, fqn: string|null}[]}
 */
function getDeclaredBeans(docText, imports, beandoc) {
    const beans = [];
    let lineStart = 0;
    while (lineStart <= docText.length) {
        let lineEnd = docText.indexOf('\n', lineStart);
        if (lineEnd < 0) lineEnd = docText.length;

        const line = docText.slice(lineStart, lineEnd);
        const firstCodeOffset = line.search(/\S/);
        if (firstCodeOffset >= 0) {
            const firstCodePos = lineStart + firstCodeOffset;
            const context = scanGroovyContext(docText, firstCodePos);
            const frame = topFrame(context);
            const m = line.slice(firstCodeOffset).match(/^(\w+)\s*\(\s*([\w.]+)\s*\)/);
            if (!context.inString && !context.inComment && frame && isBeansBlockFrame(docText, frame) && m) {
                beans.push({
                    id: m[1],
                    fqn: resolveClassName(m[2], imports, beandoc),
                });
            }
        }

        if (lineEnd === docText.length) break;
        lineStart = lineEnd + 1;
    }

    beans.sort((a, b) => a.id.localeCompare(b.id));
    return beans;
}

/**
 * Resolve the class name used in a `new ClassName(...)` expression that the
 * cursor is currently inside. Scans back from `pos` to find `new Foo(` where
 * the paren is unmatched (i.e. we are still inside that argument list).
 * @param {string} docText
 * @param {ReturnType<typeof scanGroovyContext>} context
 * @param {{ exact: Map<string,string>, wildcards: string[] }} imports
 * @param {BeanDoc} beandoc
 * @returns {string|null}
 */
function findEnclosingNewClassInContext(docText, context, imports, beandoc) {
    if (context.inString || context.inComment) return null;

    const frame = topFrame(context);
    if (!frame || frame.ch !== '(') return null;

    const before = docText.slice(0, frame.pos).trimEnd();
    const newMatch = before.match(/\bnew\s+([\w.]+)$/);
    if (!newMatch) return null;

    return resolveClassName(newMatch[1], imports, beandoc);
}

/**
 * Detect completion inside the quoted argument of ref('...').
 *
 * @param {string} docText
 * @param {number} pos
 * @param {ReturnType<typeof scanGroovyContext>} context
 * @returns {{partial: string, from: number}|null}
 */
function findRefStringContext(docText, pos, context) {
    if (!context.inString || context.stringTriple || context.stringStart < 0) return null;
    if (context.stringQuote !== "'" && context.stringQuote !== '"') return null;

    const beforeString = docText.slice(0, context.stringStart);
    if (!/\bref\s*\(\s*$/.test(beforeString)) return null;

    return {
        partial: docText.slice(context.stringStart + 1, pos),
        from: context.stringStart + 1,
    };
}

/**
 * Build class-name completion options that apply the short name and auto-insert import.
 *
 * @param {string[]} fqns
 * @param {BeanDoc} beandoc
 * @returns {import("@codemirror/autocomplete").Completion[]}
 */
function classCompletions(fqns, beandoc) {
    return fqns.map(fqn => {
        const short = fqn.replace(/.*\./, '');
        const bean = beandoc[fqn];
        return {
            label: short,
            detail: fqn,
            type: "class",
            info: () => makeDiv(bean.description),
            apply(view, completion, applyFrom, applyTo) {
                const tx = importInsertTransaction(view.state, fqn);
                if (tx) view.dispatch(view.state.update({changes: tx.changes}));
                view.dispatch(view.state.update({changes: [{from: applyFrom, to: applyTo, insert: short}]}));
            }
        };
    });
}

/**
 * Build property-name completion options for a given bean class.
 *
 * @param {string} beanClass Fully-qualified class name
 * @param {string} partial Text typed so far
 * @param {BeanDoc} beandoc
 * @returns {import("@codemirror/autocomplete").Completion[]}
 */
function propertyCompletions(beanClass, partial, beandoc) {
    const bean = beandoc[beanClass];
    if (!bean || !bean.properties) return [];
    return Object.entries(bean.properties)
        .filter(([name]) => name.startsWith(partial))
        .map(([name, prop]) => ({
            label: name,
            type: "property",
            detail: (!prop.type ? "" : stripPackage(prop.type)) +
                (prop.default !== undefined ? " = " + prop.default : ""),
            info: () => makeDiv(prop.description),
        }));
}

/**
 * Autocomplete for Heritrix Groovy DSL (Spring beans {} DSL).
 *
 * @param {BeanDoc} beandoc
 * @param {import("@codemirror/autocomplete").CompletionContext} context
 * @returns {import("@codemirror/autocomplete").CompletionResult | null}
 */
function completeHeritrixGroovy(beandoc, context) {
    const pos = context.pos;
    const docText = context.state.doc.toString();
    const textBefore = docText.slice(0, pos);
    const groovyContext = scanGroovyContext(docText, pos);

    // ---- Context 1: import statement ----------------------------------------
    if (!groovyContext.inString && !groovyContext.inComment) {
        const importMatch = textBefore.match(/\bimport\s+([\w.]*)$/);
        if (importMatch) {
            const partial = importMatch[1];
            const from = pos - partial.length;
            const matches = Object.keys(beandoc)
                .filter(fqn => fqn.startsWith(partial))
                .map(fqn => ({
                    label: fqn,
                    type: "class",
                    info: () => makeDiv(beandoc[fqn].description),
                }));
            if (!matches.length && !context.explicit) return null;
            return {from, options: matches};
        }
    }

    // ---- Context 4: ref('|') ------------------------------------------------
    // Trigger only inside the simple quoted argument of ref(...).
    const refString = findRefStringContext(docText, pos, groovyContext);
    if (refString) {
        const imports = parseImports(docText);
        const declared = getDeclaredBeans(docText, imports, beandoc);
        const matches = declared
            .filter(b => b.id.startsWith(refString.partial))
            .map(b => ({
                label: b.id,
                type: "variable",
                detail: b.fqn ? stripPackage(b.fqn) : null,
            }));
        if (!matches.length && !context.explicit) return null;
        return {from: refString.from, options: matches};
    }

    if (groovyContext.inString || groovyContext.inComment) {
        return null;
    }

    // ---- Context 5: new ClassName|  -----------------------------------------
    // Matches "new " followed by a partial class name (no open paren yet on this line).
    const newClassMatch = textBefore.match(/\bnew\s+([\w.]*)$/);
    if (newClassMatch) {
        const partial = newClassMatch[1];
        const from = pos - partial.length;
        const matches = resolveClassMatches(partial, beandoc);
        if (!matches.length && !context.explicit) return null;
        return {from, options: classCompletions(matches, beandoc)};
    }

    // ---- Context 2: bean definition argument: beanId(|) ---------------------
    // Line looks like:  "    beanId(" with cursor after the paren (single-line).
    {
        let parenDepth = 0;
        let i = pos - 1;
        let foundOpenParen = false;
        for (; i >= 0; i--) {
            const ch = docText[i];
            if (ch === ')') { parenDepth++; continue; }
            if (ch === '(') {
                if (parenDepth > 0) { parenDepth--; continue; }
                foundOpenParen = true;
                break;
            }
            if (ch === '\n') break;
        }

        if (foundOpenParen) {
            const before = docText.slice(0, i).trimEnd();
            const lineStart = before.lastIndexOf('\n') + 1;
            const linePrefix = before.slice(lineStart);
            // Must be exactly "    beanId" — an indented single identifier
            if (/^\s*\w+$/.test(linePrefix)) {
                const partial = docText.slice(i + 1, pos).trim();
                const from = i + 1 + docText.slice(i + 1, pos).match(/^\s*/)[0].length;

                const matches = resolveClassMatches(partial, beandoc);
                if (!matches.length && !context.explicit) return null;

                return {from, options: classCompletions(matches, beandoc)};
            }
        }
    }

    // ---- Contexts 3 & 6: indented bare identifier ---------------------------
    // Line looks like: "    propName" — indented identifier, nothing else on the line.
    // Activates when:
    //  - the user has typed at least one identifier character, OR
    //  - explicit invocation (Ctrl+Space), OR
    //  - the line is empty but the preceding non-whitespace character is ( or ,
    //    (i.e. the user just pressed Enter after opening a multi-line constructor
    //    or after a comma-separated argument)
    // validFor keeps the popup alive as further characters are typed, and prevents
    // Enter from being consumed as a completion confirmation.
    // Try context 6 first (new Foo named-arg): if the cursor is inside a new Foo(...)
    // argument list, offer property names with ": " applied.
    // Fall through to context 3 (bean closure property) otherwise.
    {
        const lineStart = textBefore.lastIndexOf('\n') + 1;
        const lineText = textBefore.slice(lineStart);

        const propMatch = lineText.match(/^(\s+)(\w*)$/);
        if (propMatch) {
            const partial = propMatch[2];
            const previous = previousCodeChar(docText, lineStart - 1);
            const afterOpeningPunctuation = previous === '(' || previous === ',';
            if (!partial && !context.explicit && !afterOpeningPunctuation) return null;
            const from = pos - partial.length;
            const imports = parseImports(docText);

            // Context 6: inside new Foo(...) argument list (parens, not braces)
            const newClass = findEnclosingNewClassInContext(docText, groovyContext, imports, beandoc);
            if (newClass) {
                const matches = propertyCompletions(newClass, partial, beandoc);
                if (matches.length || context.explicit) {
                    return {
                        from,
                        validFor: /^\w*$/,
                        options: matches.map(m => ({...m, apply: m.label + ': '}))
                    };
                }
            }

            // Context 3: inside beanId(Class) { ... } closure (braces)
            const beanClass = findEnclosingBeanClassInContext(docText, groovyContext, imports, beandoc);
            if (!beanClass) return null;

            const matches = propertyCompletions(beanClass, partial, beandoc);
            if (!matches.length && !context.explicit) return null;
            return {from, validFor: /^\w*$/, options: matches};
        }
    }

    return null;
}

/**
 * @param {import("@codemirror/state").EditorState} state
 * @param {BeanDoc} beandoc
 * @returns {boolean}
 */
function shouldAutoStartPropertyCompletion(state, beandoc) {
    const pos = state.selection.main.head;
    const line = state.doc.lineAt(pos);
    if (line.text.trim() !== '') return false;

    const docText = state.doc.toString();
    const context = scanGroovyContext(docText, pos);
    if (context.inString || context.inComment) return false;

    const previous = previousCodeChar(docText, Math.max(0, line.from - 1));

    const imports = parseImports(docText);
    const beanClass = findEnclosingBeanClassInContext(docText, context, imports, beandoc);
    if (beanClass && previous) return true;

    if (previous !== '(' && previous !== ',') return false;
    return !!findEnclosingNewClassInContext(docText, context, imports, beandoc);
}

/**
 * Language support for Heritrix Groovy configuration files with autocomplete.
 *
 * @param {BeanDoc} beandoc
 * @returns {import("@codemirror/state").Extension[]}
 */
export function heritrixGroovy(beandoc) {
    const groovyLang = StreamLanguage.define(groovy);

    // After a newline inside a `new Foo(...)` named-argument list or directly
    // inside a bean closure, open the completion popup automatically. The
    // context check avoids punctuation in strings, comments, and list literals.
    const newlineCompletionListener = EditorView.updateListener.of(update => {
        if (!update.docChanged) return;
        // Check if the transaction inserted a newline (the inserted text contains \n)
        let insertedNewline = false;
        update.changes.iterChanges((_fromA, _toA, _fromB, _toB, inserted) => {
            if (inserted.toString().includes('\n')) insertedNewline = true;
        });
        if (!insertedNewline) return;

        if (shouldAutoStartPropertyCompletion(update.state, beandoc)) {
            // Defer startCompletion so it runs after the current update cycle
            // has fully committed; calling it synchronously here gets cancelled.
            const view = update.view;
            requestAnimationFrame(() => startCompletion(view));
        }
    });

    return [
        groovyLang,
        groovyLang.data.of({
            autocomplete: context => completeHeritrixGroovy(beandoc, context),
        }),
        indentUnit.of("    "),
        newlineCompletionListener,
    ];
}
