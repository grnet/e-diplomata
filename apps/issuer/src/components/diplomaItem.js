import Typography from "@material-ui/core/Typography";
import Link from "next/link";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";

export default function DiplomaItem(props) {
  const url = `/diplomas/${props._id}`;
  return (
    <Link href={url}>
      <ListItem button alignItems="flex-start">
        <ListItemText
          secondary={
            <Typography variant="body2" color="textPrimary">
              Τίτλος Σπουδών:{" "}
              <>
                <strong>{props.title}</strong> |{" "}
              </>
             Είδος τίτλου Σπουδών:{" "}
              <>
                <strong>{props.type}</strong> |{" "}
              </> 
              Τμήμα/Σχολή:{" "}
              <>
                <strong>{props.department}</strong> |{" "}
              </>
              </Typography>
          }
        />
      </ListItem>
    </Link>
  );
}
