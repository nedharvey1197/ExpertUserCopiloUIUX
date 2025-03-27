import React from "react";

export function Card({ children }) {
  return <div className="bg-white rounded-2xl shadow-md p-4">{children}</div>;
}

export function CardContent({ children }) {
  return <div className="p-2">{children}</div>;
}