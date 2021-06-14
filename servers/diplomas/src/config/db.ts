
import mongoose from "mongoose";

// Replace this with your MONGOURI.
const MONGOURI = process.env.MONGOURI || "mongodb://0.0.0.0:27017";

export const InitiateMongoServer = async (uri?:string) => {
  try {
    return await mongoose.connect(uri || MONGOURI, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
  } catch (e) {
    console.log(e);
    throw e;
  }
};

