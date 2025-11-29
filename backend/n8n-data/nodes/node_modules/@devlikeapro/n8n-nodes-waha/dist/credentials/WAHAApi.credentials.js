"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.WAHAApi = void 0;
class WAHAApi {
    constructor() {
        this.name = 'wahaApi';
        this.displayName = 'WAHA API';
        this.properties = [
            {
                displayName: 'Host URL',
                name: 'url',
                type: 'string',
                default: 'http://localhost:3000',
            },
            {
                displayName: 'API Key',
                name: 'apiKey',
                type: 'string',
                typeOptions: { password: true },
                default: '',
                required: false,
            }
        ];
        this.authenticate = {
            type: 'generic',
            properties: {
                headers: {
                    'X-Api-Key': '={{$credentials.apiKey}}',
                },
            },
        };
        this.test = {
            request: {
                baseURL: '={{$credentials.url}}',
                url: '/api/sessions',
            },
        };
    }
}
exports.WAHAApi = WAHAApi;
//# sourceMappingURL=WAHAApi.credentials.js.map