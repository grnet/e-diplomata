import Typography from "@material-ui/core/Typography";
import Link from "next/link";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";

export default function SharedTitleItem(props) {
    const url = `/shares/${props._id}`;
    return (
        <Link href={url}>
            <ListItem button alignItems="flex-start">
                <ListItemText
                    secondary={
                        <Typography variant="body2" color="textPrimary">
                            Όνομα:{" "}
                            <>
                                <strong>{props.firstName}</strong> |{" "}
                            </>
                            Επώνυμο:{" "}
                                <>
                                    <strong>{props.lastName}</strong> |{" "}
                                </>
                            Status:{" "}
                                <>
                                    <strong>{props.status}</strong> 
                                </>
                        </Typography>
                    }
                />
            </ListItem>
        </Link>
    );
}
