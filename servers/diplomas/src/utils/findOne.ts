export const findOneFactory = (query, Model)=>{
  return async function(req, res){
    const data = await Model.findOne(query(req)).exec()
    res.json(data)
  }
}