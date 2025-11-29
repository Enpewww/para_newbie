"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WAHA = void 0;
const n8n_workflow_1 = require("n8n-workflow");
const WAHAv202409_1 = require("./v202409/WAHAv202409");
const node_1 = require("./base/node");
const WAHAv202502_1 = require("./v202502/WAHAv202502");
class WAHA extends n8n_workflow_1.VersionedNodeType {
    constructor() {
        const baseDescription = {
            ...node_1.BASE_DESCRIPTION,
            defaultVersion: 202502,
        };
        const nodeVersions = {
            202502: new WAHAv202502_1.WAHAv202502(),
            202409: new WAHAv202409_1.WAHAv202409(),
        };
        super(nodeVersions, baseDescription);
    }
}
exports.WAHA = WAHA;
//# sourceMappingURL=WAHA.node.js.map