import generateWallet from '../generateWallet';
import deployContract from '../deployContract';
import { getTransactionSync } from '../getTransaction';
import { ABI, Bytecode } from '../contracts/Award';
import { publish } from '../publish';
import * as ethers from 'ethers';
jest.setTimeout(60000);
const signature =
  '81c1eee27c3af6b85037b7f2198130b1abcefcfba489a9a2d489c9aa4ab1a76b61faba9f8e8194846a70048a9ff1af8810a11981fc31411032fcf5e9a6c9b4609a584ee3f09e9a0198ea5e1c75a04e8715b25af7a1418800d0cfa4205e4b1576';
type Provider = {
  provider: 'ganache' | 'infura';
  network: string;
  providerOptions: any;
};
const provider: Provider = {
  provider: 'infura',
  network: 'ropsten',
  providerOptions: {
    etherscan: 'GCQC14SVVI1SAI147SWIPS5HIVSH3HGKPH',
    infura: {
      projectId: '7c7378ab4bfd4e0e8450f6eb2f581aa6',
      projectSecret: 'a1d95592810f45f8959010c24efaf543',
    },
  },
};
const walletWithEther = new ethers.Wallet(
  `365c49f1e59341446c9b648505ee9fb5c538276ea6e42be0b53b76309aad27df`
);
const options = {} as any;
describe('test ledger lib with ganache ', () => {
  it('should generate a wallet private and public key', async () => {
    const { private: key, public: wallet } = await generateWallet({
      networkType: 'infura',
      party: 'Issuer',
    });
    options.account = walletWithEther.privateKey;
    options.address = walletWithEther.address;
    expect(key).toBeDefined();
    expect(wallet).toBeDefined();
  });
  it('should deploy a contract', async () => {
    const result = await deployContract({
      ...provider,
      abi: ABI,
      bytecode: Bytecode,
      account: options.account,
    });
    options.contractAddress = result.address;
    options.contractHash = result.hash;
    expect(result.address).toBeDefined();
    expect(result.hash).toBeDefined();
  });
  it('should wait for the deploy transaction to finish', async () => {
    const tx = await getTransactionSync({
      ...provider,
      hash: options.contractHash,
      minConfirmations: 2,
    });
    expect(tx.status).not.toBe('pending');
  });
  it('should run a publish transaction and return the hash immediately', async () => {
    const publishTx = await publish({
      abi: ABI,
      address: options.contractAddress,
      signature,
      account: options.account,
      ...provider,
    });
    options.publishHash = publishTx.hash;
    expect(publishTx.hash).toBeDefined();
  });
  it('should wait for the publish transaction to return the signature data', async () => {
    const tx = await getTransactionSync({
      ...provider,
      hash: options.publishHash,
      minConfirmations: 2,
      abi: ABI,
    });
    expect(tx.status).toBe('confirmed');
    expect(tx.data).toBe(signature);
  });
});
