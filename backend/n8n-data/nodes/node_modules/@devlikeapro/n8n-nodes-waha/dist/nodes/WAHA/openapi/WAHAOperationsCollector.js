"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WAHAOperationsCollector = void 0;
const n8n_openapi_node_1 = require("@devlikeapro/n8n-openapi-node");
function sessionFirst(a, b) {
    if (a.name === 'session') {
        return -1;
    }
    if (b.name === 'session') {
        return 1;
    }
    return 0;
}
class WAHAOperationsCollector extends n8n_openapi_node_1.OperationsCollector {
    parseFields(operation, context) {
        const fields = super.parseFields(operation, context);
        fields.sort(sessionFirst);
        return fields;
    }
}
exports.WAHAOperationsCollector = WAHAOperationsCollector;
//# sourceMappingURL=WAHAOperationsCollector.js.map