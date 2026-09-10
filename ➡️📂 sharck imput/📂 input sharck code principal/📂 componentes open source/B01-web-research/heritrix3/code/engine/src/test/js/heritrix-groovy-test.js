#!/usr/bin/env node

const assert = require('assert')
const fs = require('fs')
const path = require('path')
const vm = require('vm')

const repoRoot = path.resolve(__dirname, '../../../..')
const sourcePath = path.join(repoRoot,
    'engine/src/main/resources/org/archive/crawler/restlet/js/heritrix-groovy.js')

const source = fs.readFileSync(sourcePath, 'utf8')
    .replace(/^import .*$/gm, '')
    .replace(/^export function heritrixGroovy/gm, 'function heritrixGroovy')
    + `
Object.assign(globalThis, {
    completeHeritrixGroovy,
    findEnclosingBeanClassInContext,
    findEnclosingNewClassInContext,
    findRefStringContext,
    previousCodeChar,
    scanGroovyContext,
    shouldAutoStartPropertyCompletion,
});
`

const sandbox = {
    console,
    document: {createElement: () => ({})},
    requestAnimationFrame: () => {},
}
vm.createContext(sandbox)
vm.runInContext(source, sandbox, {filename: sourcePath})

const beandoc = {
    'org.archive.crawler.prefetch.Preselector': {
        properties: {
            allowByRegex: {type: 'java.lang.String'},
            blockByRegex: {type: 'java.lang.String'},
        },
    },
    'org.archive.crawler.prefetch.FrontierPreparer': {
        properties: {
            preferenceDepthHops: {type: 'int'},
        },
    },
    'org.archive.modules.deciderules.SurtPrefixedDecideRule': {
        properties: {
            decision: {type: 'java.lang.String'},
            seedsAsSurtPrefixes: {type: 'boolean'},
            surtsDumpFile: {type: 'org.archive.spring.ConfigFile'},
        },
    },
    'org.archive.modules.deciderules.TooManyHopsDecideRule': {
        properties: {
            maxHops: {type: 'int'},
        },
    },
}

function stateAt(markedText) {
    const pos = markedText.indexOf('|')
    assert.notStrictEqual(pos, -1, 'test fixture must mark the cursor with |')

    const text = markedText.slice(0, pos) + markedText.slice(pos + 1)
    const lineStarts = [0]
    for (let i = 0; i < text.length; i++) {
        if (text[i] === '\n') lineStarts.push(i + 1)
    }

    return {
        selection: {main: {head: pos}},
        doc: {
            toString: () => text,
            lineAt(position) {
                let from = 0
                for (const start of lineStarts) {
                    if (start > position) break
                    from = start
                }
                let to = text.indexOf('\n', from)
                if (to < 0) to = text.length
                return {from, to, text: text.slice(from, to)}
            },
        },
    }
}

function completionContextAt(markedText, explicit = false) {
    const state = stateAt(markedText)
    return {
        explicit,
        pos: state.selection.main.head,
        state,
    }
}

function labels(result) {
    return Array.from(result ? result.options : [], option => option.label)
}

function assertAutoStart(name, markedText, expected) {
    assert.strictEqual(
        sandbox.shouldAutoStartPropertyCompletion(stateAt(markedText), beandoc),
        expected,
        name)
}

function assertCompletionLabels(name, markedText, expectedLabels, explicit = false) {
    assert.deepStrictEqual(
        labels(sandbox.completeHeritrixGroovy(beandoc, completionContextAt(markedText, explicit))),
        expectedLabels,
        name)
}

assertAutoStart('bean opening brace auto-starts',
    "import org.archive.crawler.prefetch.*\npreselector(Preselector) {\n    |",
    true)

assertAutoStart('bean property assignment auto-starts',
    "import org.archive.crawler.prefetch.*\npreselector(Preselector) {\n    allowByRegex = \"moo\"\n    |",
    true)

assertAutoStart('constructor opening paren auto-starts',
    "import org.archive.modules.deciderules.*\nnew TooManyHopsDecideRule(\n    |",
    true)

assertAutoStart('constructor comma auto-starts',
    "import org.archive.modules.deciderules.*\nnew SurtPrefixedDecideRule(\n    decision: 'REJECT',\n    |",
    true)

assertAutoStart('list comma does not auto-start',
    "processors = [\n    ref('preselector'),\n    |",
    false)

assertAutoStart('nested list inside constructor does not auto-start',
    "import org.archive.modules.deciderules.*\nnew SurtPrefixedDecideRule(\n    decision: [\n        'REJECT',\n        |",
    false)

assertAutoStart('triple-quoted string does not auto-start',
    "import org.archive.modules.deciderules.*\nnew TooManyHopsDecideRule(\n    note: '''hello,\n    |",
    false)

assertAutoStart('slashy string does not auto-start',
    "import org.archive.modules.deciderules.*\nnew SurtPrefixedDecideRule(\n    decision: /ACCEPT,\n    |",
    false)

assertAutoStart('dollar-slashy string does not auto-start',
    "import org.archive.modules.deciderules.*\nnew SurtPrefixedDecideRule(\n    decision: $/ACCEPT,\n    |",
    false)

assertAutoStart('division is not treated as slashy string',
    "import org.archive.modules.deciderules.*\nnew TooManyHopsDecideRule(\n    maxHops: 12 / 3,\n    |",
    true)

assertCompletionLabels('bean property labels after return',
    "import org.archive.crawler.prefetch.*\npreselector(Preselector) {\n    allowByRegex = \"moo\"\n    |",
    ['allowByRegex', 'blockByRegex'],
    true)

assertCompletionLabels('constructor property labels after comma',
    "import org.archive.modules.deciderules.*\nnew SurtPrefixedDecideRule(\n    decision: 'REJECT',\n    |",
    ['decision', 'seedsAsSurtPrefixes', 'surtsDumpFile'],
    true)

assertCompletionLabels('list literal has no property labels',
    "processors = [\n    ref('preselector'),\n    |",
    [],
    true)

assertCompletionLabels('ref labels include differently indented top-level beans only',
    "import org.archive.crawler.prefetch.*\n" +
    "beans {\n" +
    "  preselector(Preselector) {\n" +
    "  }\n" +
    "\tpreparer(FrontierPreparer)\n" +
    "  processors = [\n" +
    "    nestedLookalike(Preselector)\n" +
    "  ]\n" +
    "  // commentedLookalike(Preselector)\n" +
    "  ref('pre|')\n" +
    "}",
    ['preparer', 'preselector'])

console.log('heritrix-groovy context tests passed')
