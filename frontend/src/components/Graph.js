import React, { useState } from "react";
import "chart.js/auto";
import { Line } from "react-chartjs-2";
// import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/solid';

const Graph = () => {
  const [startIndex, setStartIndex] = useState(0);
  const [endIndex, setEndIndex] = useState(4);

  const data = {
    labels: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
    datasets: [
      {
        label: "Daily Sales",
        data: [100, 150, 200, 180, 250, 300, 280, 350, 400, 380, 450, 500],
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        grid: {
          display: false,
        },
      },
    },
  };

  const handlePrevious = () => {
    if (startIndex > 0) {
      setStartIndex(startIndex - 5);
      setEndIndex(endIndex - 5);
    }
  };

  const handleNext = () => {
    if (endIndex < data.labels.length - 1) {
      setStartIndex(startIndex + 5);
      setEndIndex(endIndex + 5);
    }
  };

  return (
    <div>
      <div>
        <button onClick={handlePrevious}>
          {/* <ChevronLeftIcon /> */}
          <p>LEFT</p>
        </button>
        <button onClick={handleNext}>
          {/* <ChevronRightIcon /> */}
          <p>RIGHT</p>
        </button>
      </div>
      <div className="w-full h-1/2">
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

export default Graph;
