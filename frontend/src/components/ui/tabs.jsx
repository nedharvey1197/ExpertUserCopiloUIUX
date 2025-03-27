import React, { useState } from "react";

export function Tabs({ defaultValue, children }) {
  const [value, setValue] = useState(defaultValue);
  return React.Children.map(children, (child) =>
    React.cloneElement(child, { value, setValue })
  );
}

export function TabsList({ children }) {
  return <div className="flex gap-2 mb-4">{children}</div>;
}

export function TabsTrigger({ value: triggerValue, value, setValue, children }) {
  return (
    <button
      className={`px-3 py-1 rounded-md text-sm ${
        triggerValue === value ? "bg-blue-600 text-white" : "bg-gray-100"
      }`}
      onClick={() => setValue(triggerValue)}
    >
      {children}
    </button>
  );
}

export function TabsContent({ value, children, value: tabValue }) {
  return value === tabValue ? <div>{children}</div> : null;
}