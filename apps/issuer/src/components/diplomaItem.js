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
              Όνομα:{" "}
              <>
                <strong>{props.userName}</strong> |{" "}
              </>
              Τίτλος Σπουδών:{" "}
              <>
                <strong>{props.degree}</strong> |{" "}
              </>
              Είδος τίτλου Σπουδών:{" "}
              <>
                <strong>{props.typeOfDegree}</strong> |{" "}
              </>
              Τμήμα/Σχολή:{" "}
              <>
                <strong>{props.school}</strong> |{" "}
              </>
              Ίδρυμα:{" "}
              <>
                <strong>{props.institution}</strong> |{" "}
              </>
              Έτος:{" "}
              <>
                <strong>{props.year}</strong> |{" "}
              </>
              Status:{" "}
              <>
                <strong>{props.status}</strong> |{" "}
              </>
            </Typography>
          }
        />
      </ListItem>
    </Link>
  );
}
