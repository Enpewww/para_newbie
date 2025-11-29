import { INodeTypeBaseDescription, NodeConnectionType } from "n8n-workflow";
export declare const BASE_DESCRIPTION: INodeTypeBaseDescription;
export declare const NODE_DESCRIPTION: {
    subtitle: string;
    inputs: NodeConnectionType[];
    outputs: NodeConnectionType[];
    defaults: {
        name: string;
    };
    credentials: {
        name: string;
        required: boolean;
    }[];
    requestDefaults: {
        headers: {
            Accept: string;
            'Content-Type': string;
        };
        baseURL: string;
    };
};
