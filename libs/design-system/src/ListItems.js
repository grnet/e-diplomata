import React from "react";
import Typography from "@material-ui/core/Typography";
import Link from "next/link";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";


export default function ListItems({row, presentation}) {
  const url = presentation.url(row);
  return (
    <Link href={url}>
      <ListItem button alignItems="flex-start">
        <ListItemText
          secondary={
            <Typography variant="body2" color="textPrimary">
              {presentation.fields.map(field=>{
                return (
                  <>
                    {field.label}: <strong>{row[field.key]}</strong> |{" "}
                  </>
                )
              })}
            
              </Typography>
          }
        />
      </ListItem>
    </Link>
  );
}
