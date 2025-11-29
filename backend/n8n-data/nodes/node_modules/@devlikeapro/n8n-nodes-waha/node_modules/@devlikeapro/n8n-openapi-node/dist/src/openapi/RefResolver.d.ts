import { OpenAPIV3 } from "openapi-types";
export declare class RefResolver {
    private doc;
    constructor(doc: any);
    /**
     * Resolve ref and return it if found
     * @param schema
     */
    resolveRef<T>(schema: OpenAPIV3.ReferenceObject | T): [T, string[]?];
    resolve<T>(schema: OpenAPIV3.ReferenceObject | T): T;
    private findRef;
}
