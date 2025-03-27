import React from "react";

export function Textarea(props) {
  return (
    <textarea
      {...props}
      className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm"
    />
  );
}