import { issuerCredentials } from '@diplomas/server/utils/dummy_credentials';

export default {
    get:[async function (_req: any, res: any) {
        res.json(issuerCredentials);
    }]
}

