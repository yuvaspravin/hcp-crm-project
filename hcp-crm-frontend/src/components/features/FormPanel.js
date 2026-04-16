import React from "react";
import { useSelector } from "react-redux";

const FormPanel = () => {
  const formState = useSelector((state) => state.form);

  return (
    <div
      className="w-1/2 p-6 bg-gray-50 border-r overflow-y-auto"
      style={{ fontFamily: "Inter, sans-serif" }}
    >
      <h2 className="text-2xl font-bold mb-6 border-b pb-2">
        Log HCP Interaction
      </h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            HCP Name
          </label>
          <input
            type="text"
            readOnly
            value={formState.hcpName}
            className="mt-1 block w-full rounded-md border-gray-300 bg-white p-2 border shadow-sm"
            placeholder="Search or select HCP..."
          />
        </div>

        <div className="flex space-x-4">
          <div className="w-1/2">
            <label className="block text-sm font-medium text-gray-700">
              Date
            </label>
            <input
              type="date"
              readOnly
              value={formState.date}
              className="mt-1 block w-full rounded-md border-gray-300 bg-white p-2 border shadow-sm"
            />
          </div>
          <div className="w-1/2">
            <label className="block text-sm font-medium text-gray-700">
              Time
            </label>
            <input
              type="time"
              readOnly
              value={formState.time}
              className="mt-1 block w-full rounded-md border-gray-300 bg-white p-2 border shadow-sm"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Topics Discussed
          </label>
          <textarea
            readOnly
            value={formState.topicsDiscussed}
            rows="3"
            className="mt-1 block w-full rounded-md border-gray-300 bg-white p-2 border shadow-sm"
            placeholder="Enter key discussion points..."
          ></textarea>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Materials Shared
          </label>
          <div className="mt-1 block w-full rounded-md border-gray-300 bg-white p-2 border shadow-sm min-h-[40px] text-sm text-gray-500">
            {formState.materialsShared.length > 0
              ? formState.materialsShared.join(", ")
              : "No materials added."}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Observed/Inferred HCP Sentiment
          </label>
          <div className="mt-2 flex items-center space-x-4">
            {["Positive", "Neutral", "Negative"].map((sentiment) => (
              <label key={sentiment} className="inline-flex items-center">
                <input
                  type="radio"
                  readOnly
                  checked={formState.sentiment === sentiment}
                  className="form-radio text-blue-600"
                />
                <span className="ml-2 text-sm text-gray-700">{sentiment}</span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            Follow-up Actions
          </label>
          <ul className="list-disc pl-5 mt-1 text-sm text-blue-600">
            {formState.followUpActions.length > 0 ? (
              formState.followUpActions.map((action, i) => (
                <li key={i}>{action}</li>
              ))
            ) : (
              <span className="text-gray-500 list-none ml-[-20px]">
                No follow-ups suggested yet.
              </span>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default FormPanel;
