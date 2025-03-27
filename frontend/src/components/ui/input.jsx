import React from "react";

export function Input(props) {
  return (
    <input
      {...props}
      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
    />
  );
}
