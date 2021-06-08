import jwt from "jsonwebtoken";


export default function authFactory(Model: any) {
  console.log(Model.modelName);
  return async function jwtMiddleware(req: any, res: any, next: any) {
    const token = req.header("Authorization").split('Token ')[1];
    if (!token) return res.status(401).json({ message: "Auth Error" });

    try {
      const decoded = jwt.verify(token, "randomString") as any;
      const user = await Model.findById(decoded.user.id)
      req.user = user;
      next();
    } catch (e) {
      console.error(e);
      res.status(500).send({ message: "Invalid Token" });
    }
  }
};