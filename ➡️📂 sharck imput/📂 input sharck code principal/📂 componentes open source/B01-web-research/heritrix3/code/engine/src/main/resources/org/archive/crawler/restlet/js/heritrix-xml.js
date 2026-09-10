 /**
 * Heritrix XML (Spring beans CXML) language support for CodeMirror.
 *
 * Exports a single factory function `heritrixXml(beandoc)` that returns a
 * CodeMirror LanguageSupport extension with Heritrix-aware autocomplete.
 *
 * Autocomplete contexts:
 *  - Tag names inside known Spring XML elements (bean, property, list, …)
 *  - Attribute names for each element type
 *  - class= on <bean>: suggests fully-qualified Heritrix class names from beandoc
 *  - name= on <property>: suggests property names for the enclosing bean's class
 *  - bean= on <ref>: suggests bean ids declared in the document
 */

import {LanguageSupport, syntaxTree} from "@codemirror/language"
import {autoCloseTags, xmlLanguage} from "@codemirror/lang-xml"

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

const TAG_COMPLETIONS = {
    "beans": ["bean"],
    "bean": ["constructor-arg", "property"],
    "constructor-arg": ["bean", "list", "map", "ref", "value"],
    "property": ["bean", "list", "map", "ref", "value"],
    "map": ["entry"],
    "list": ["bean", "list", "map", "ref", "value"],
};

const ATTRIBUTE_COMPLETIONS = {
    "bean": ["class", "id"],
    "constructor-arg": ["value"],
    "property": ["name", "value"],
    "ref": ["bean"],
    "entry": ["key", "value"],
};

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
 * Calculate auto-completions for Heritrix XML.
 *
 * @param {BeanDoc} beandoc
 * @param {import("@codemirror/autocomplete").CompletionContext} context
 * @returns {import("@codemirror/autocomplete").CompletionResult | null}
 */
function completeHeritrixXml(beandoc, context) {
    function slice(node) {
        if (!node) return null;
        return context.state.sliceDoc(node.from, node.to);
    }

    function getAttrValue(element, attr) {
        console.assert(element.name === 'Element', "Expected element node");
        let openTag = element.getChild('OpenTag');
        for (let attribute of openTag.getChildren('Attribute')) {
            if (slice(attribute.getChild('AttributeName')) === attr) {
                let text = slice(attribute.getChild('AttributeValue'));
                if (text.startsWith("\"") || text.startsWith("\'")) {
                    text = text.substring(1, text.length - 1);
                }
                return text;
            }
        }
        return null;
    }

    function getAttrNames(element) {
        console.assert(element.name === 'Element', "Expected element node");
        let openTag = element.getChild('OpenTag');
        let names = [];
        for (let attribute of openTag.getChildren('Attribute')) {
            names.push(slice(attribute.getChild('AttributeName')));
        }
        return names;
    }

    function getElementName(element) {
        if (!element) return null;
        let openTag = element.getChild('OpenTag');
        if (openTag) return slice(openTag.getChild('TagName'));
        return null;
    }

    function closest(node, tag) {
        while (node) {
            if (node.name === 'Element') {
                if (!tag || getElementName(node) === tag) return node;
            }
            node = node.parent;
        }
        return null;
    }

    /**
     * Get all beans declared in the document that have an id.
     * @returns {{id: string, class: string}[]}
     */
    function getDeclaredBeans() {
        const beans = []
        const cursor = syntaxTree(context.state).cursor();
        while (cursor.next()) {
            if (cursor.name === "Element") {
                let openTag = cursor.node.getChild('OpenTag');
                if (openTag && slice(openTag.getChild('TagName')) === "bean") {
                    let id = getAttrValue(cursor.node, "id");
                    if (id) beans.push({id, class: getAttrValue(cursor.node, "class")});
                }
            }
        }
        beans.sort((a, b) => a.id.localeCompare(b.id));
        return beans;
    }

    let node = syntaxTree(context.state).resolveInner(context.pos, -1)
    if (node.name === "TagName" || node.name === "StartTag") {
        let parentElement = closest(node.parent.parent.parent);
        let tag = getElementName(parentElement);
        let completions = TAG_COMPLETIONS[tag];
        if (!completions) return;
        let text = node.name === "StartTag" ? "" : context.state.sliceDoc(node.from, context.pos);
        return {
            from: context.pos - text.length,
            options: completions.filter(c => c.startsWith(text))
                .map(c => ({label: c, apply: c}))
        }
    } else if (node.name === "OpenTag" || node.name === "AttributeName") {
        let element = node.name === "OpenTag" ? node.parent : node.parent.parent.parent;
        const tag = getElementName(element);
        const existingAttrs = getAttrNames(element);
        let completions = ATTRIBUTE_COMPLETIONS[tag];
        if (!completions) return;
        let text = node.name === "OpenTag" ? "" : context.state.sliceDoc(node.from, context.pos);
        return {
            from: context.pos - text.length,
            options: completions.filter(c => c.startsWith(text) && !existingAttrs.includes(c))
                .map(c => ({label: c, apply: c + '="', reactivate: true}))
        }
    } else if (node.name === "AttributeValue") {
        let text = context.state.sliceDoc(node.from, context.pos);
        let quote = "";
        if (text.startsWith("\"") || text.startsWith("\'")) {
            quote = text.charAt(0);
            text = text.substring(1, text.length);
        }

        let matches = [];
        const tag = slice(node.parent.parent.getChild('TagName'));
        const attr = slice(node.parent.getChild('AttributeName'));
        if (tag === "bean" && attr === "class") {
            matches = Object.entries(beandoc)
                .filter(([className]) => className.includes(text))
                .map(([className, bean]) => ({
                    label: className,
                    type: "class",
                    info: () => makeDiv(bean.description),
                    apply: className + quote
                }));
        } else if (tag === "property" && attr === "name") {
            const beanElement = closest(node, "bean");
            if (!beanElement) return;
            const beanClass = getAttrValue(beanElement, "class");
            if (!beanClass) return;
            const bean = beandoc[beanClass];
            if (!bean) return;
            matches = Object.entries(bean.properties)
                .filter(([name]) => name.includes(text))
                .map(([name, prop]) => ({
                    label: name,
                    type: "property",
                    detail: (!prop.type ? "" : stripPackage(prop.type)) +
                        (prop.default ? " = " + prop.default : ""),
                    info: () => makeDiv(prop.description),
                }));
        } else if (tag === "ref" && attr === "bean") {
            matches = getDeclaredBeans()
                .filter(bean => bean.id.includes(text))
                .map(bean => ({
                    label: bean.id,
                    type: "variable",
                    detail: bean.class ? stripPackage(bean.class) : null,
                }));
        }
        return {
            from: context.pos - text.length,
            options: matches
        };
    }
}

/**
 * Language support for Heritrix XML configuration files with autocomplete functionality.
 *
 * @param {BeanDoc} beandoc The bean documentation object.
 * @return {LanguageSupport}
 */
export function heritrixXml(beandoc) {
    return new LanguageSupport(xmlLanguage, [xmlLanguage.data.of({
        autocomplete: context => completeHeritrixXml(beandoc, context),
    }), autoCloseTags]);
}
