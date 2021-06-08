
export type StorageEntry = {id: string} & unknown;

export interface StorageInterface {
  create: (type: string, data: unknown)=> StorageEntry;
  getBy: (type: string, query: unknown)=> StorageEntry;
  update: (type: string, id:string, data: unknown)=> StorageEntry;
}


