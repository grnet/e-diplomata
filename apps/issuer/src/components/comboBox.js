import React, { useEffect } from "react";
/* import React from "react"; */
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Autocomplete from "@material-ui/lab/Autocomplete";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(1),
    width: "20vw",
  },
  selectEmpty: {
    marginTop: theme.spacing(2),
  },
}));

// validate props
ComboBox.propTypes = {
  placeholder: PropTypes.string,
  value: PropTypes.object,
  options: PropTypes.array.isRequired,
  variant: PropTypes.string,
  onChange: PropTypes.func,
  autoComplete: PropTypes.bool,
};

ComboBox.defaultProps = {
  placeholder: null,
  value: null,
  options: [],
  variant: "outlined",
  autoComplete: false,
};

// checks for equality
function checkSelected(option, value) {
  return (option.value || null) === (value || null);
}

// define component
export default function ComboBox(props) {
  const classes = useStyles();
  const [value, setValue] = React.useState();

  function changeValue(e, value) {
    console.log("props value is ");
    if (props.onChange) {
      if (value === null) {
        props.onChange({ value: props.value }, props.options, true);
      } else {
        setValue(value);
        props.onChange(value, props.options, false);
      }
    }
  }

  return (
    <div>
      <Autocomplete
        className={classes.formControl}
        value={props.value}
        autoComplete={props.autoComplete}
        onChange={changeValue}
        options={props.options}
        getOptionSelected={checkSelected}
        getOptionLabel={(option) => option.label || ""}
        style={{ width: "80%" }}
        renderInput={(params) => (
          <TextField
            {...params}
            label={props.placeholder}
            variant={props.variant}
          />
        )}
      />
    </div>
  );
}
