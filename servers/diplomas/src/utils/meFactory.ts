import auth from "../middlewares/auth";

export default function meFactory(Model: any){
  return [
    auth(Model),
    async (req: any, res: any) => {
      try {
        // request.user is getting fetched from Middleware after token authentication
        const user = await Model.findById(req.user.id);
        res.json(user);
      } catch (e) {
        res.send({ message: "Error in Fetching user" });
      }
    }
  ]
}