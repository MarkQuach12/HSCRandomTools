import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { toast } from 'react-toastify';

type Prediction = {
  year: number;
  predicted_mark: number;
};

const subjects = [
  {
    label: "Mathematics",
    items: [
      "Mathematics Standard",
      "Mathematics Advanced",
      "Mathematics Extension 1",
      "Mathematics Extension 2",
    ],
  },
  {
    label: "English",
    items: ["English Advanced"],
  },
  {
    label: "Science",
    items: ["Biology", "Chemistry", "Physics"],
  },
  {
    label: "HSIE",
    items: ["Business Studies", "Economics", "Modern History"],
  },
];

function Predict() {
  const [subject, setSubject] = useState("");
  const [rawMark, setRawMark] = useState("");
  const [predictions, setPredictions] = useState<Prediction[]>([]);

  const handleSubmit = async () => {
    if (parseFloat(rawMark) < 0 || parseFloat(rawMark) > 100) {
      toast.error("Please enter a valid raw mark between 0 and 100", {
        position: "bottom-right",
        autoClose: 4000,
        hideProgressBar: false,
        theme: "colored",
      });
      return;
    }

    try {
      const response = await fetch(
        `${import.meta.env.VITE_REACT_APP_BACKEND_URL}/predict`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            subject: subject,
            rawMark: parseFloat(rawMark),
          }),
        }
      );

      const data = await response.json();

      if (response.ok) {
        setPredictions(data.predictions);
      } else {
        throw new Error(data.message);
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error(error);
        alert(error.message);
      } else {
        console.error("Unknown error:", error);
        alert("An unexpected error occurred.");
      }
    }
  };

  return (
    <div className="flex flex-col items-center p-6">
      <Card className="w-full max-w-3xl min-h-[300px] p-8">
        <CardHeader>
          <CardTitle className="text-2xl font-bold">
            HSC Scaled Mark Predictor
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Select onValueChange={setSubject} value={subject}>
            <SelectTrigger className="w-[280px]">
              <SelectValue placeholder="Select a subject" />
            </SelectTrigger>
            <SelectContent>
              {subjects.map((group) => (
                <SelectGroup key={group.label}>
                  <SelectLabel className="font-semibold">
                    {group.label}
                  </SelectLabel>
                  {group.items.map((subject) => (
                    <SelectItem key={subject} value={subject}>
                      {subject}
                    </SelectItem>
                  ))}
                </SelectGroup>
              ))}
            </SelectContent>
          </Select>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit();
            }}
          >
            <Input
              type="number"
              placeholder="Enter Raw Mark"
              className="mt-2"
              value={rawMark}
              onChange={(e) => setRawMark(e.target.value)}
            />
            <Button
              className="w-full mt-4"
              variant="outline"
            >
              Predict Scaled Mark
            </Button>
          </form>

          {predictions.length > 0 && (
            <div className="mt-6">
              <h3 className="text-lg font-semibold mb-2">Predictions</h3>
              <ul className="space-y-1">
                {predictions.map((item, index) => (
                  <li key={index}>
                    {item.year} : <strong>{item.predicted_mark}</strong>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default Predict;
