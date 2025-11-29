"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.WAHAv202502 = void 0;
const doc = __importStar(require("./openapi.json"));
const node_1 = require("../base/node");
const WAHAOperationsCollector_1 = require("../openapi/WAHAOperationsCollector");
const n8n_openapi_node_1 = require("@devlikeapro/n8n-openapi-node");
const WAHAOperationParser_1 = require("../openapi/WAHAOperationParser");
const WAHAResourceParser_1 = require("../openapi/WAHAResourceParser");
const customDefaults = [
    {
        find: {
            name: 'session',
            required: true,
            type: 'string',
        },
        replace: {
            default: '={{ $json.session }}',
        },
    },
    {
        find: {
            name: 'chatId',
            required: true,
            type: 'string',
        },
        replace: {
            default: '={{ $json.payload.from }}',
        },
    },
    {
        find: {
            name: 'messageId',
            type: 'string',
        },
        replace: {
            default: '={{ $json.payload.id }}',
        },
    },
    {
        find: {
            name: 'reply_to',
            type: 'string',
        },
        replace: {
            default: '',
        },
    },
];
const config = {
    OperationsCollector: WAHAOperationsCollector_1.WAHAOperationsCollector,
    operation: new WAHAOperationParser_1.WAHAOperationParser(),
    resource: new WAHAResourceParser_1.WAHAResourceParser(),
};
const parser = new n8n_openapi_node_1.N8NPropertiesBuilder(doc, config);
const properties = parser.build(customDefaults);
class WAHAv202502 {
    constructor() {
        this.description = {
            ...node_1.BASE_DESCRIPTION,
            ...node_1.NODE_DESCRIPTION,
            version: 202502,
            properties: properties,
        };
    }
}
exports.WAHAv202502 = WAHAv202502;
//# sourceMappingURL=WAHAv202502.js.map