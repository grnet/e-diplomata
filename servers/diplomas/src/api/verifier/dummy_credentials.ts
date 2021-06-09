import { verifierCredentials } from '@diplomas/server/utils/dummy_credentials';

export default {
    get:[async function (req: any, res: any) {
        console.log(req)
        res.json(verifierCredentials);
    }]
}

