import { OpenAPIV3 } from 'openapi-types';
import { DefaultResourceParser } from '@devlikeapro/n8n-openapi-node';
export declare class WAHAResourceParser extends DefaultResourceParser {
    value(tag: OpenAPIV3.TagObject): string;
}
