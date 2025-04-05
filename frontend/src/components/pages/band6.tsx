import { useState } from 'react';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

function Band6() {
  const [school, setSchool] = useState('');
  const [subjectData, setSubjectData] = useState<any[]>([]);
  const [years, setYears] = useState<string[]>([]);

  const handleSubmit = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_REACT_APP_BACKEND_URL}/band6`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ school }),
      });

      const data = await response.json();

      if (response.ok) {
        const raw = data.school_data;

        const sampleSubject = Object.values(raw)[0] as Record<string, number>;
        const yearKeys = Object.keys(sampleSubject);

        const reversedYears = [...yearKeys].reverse(); // make a copy before reversing
        setYears(reversedYears);


        const transformed = Object.entries(raw).map(([subject, yearData]: any) => ({
            subject, ...yearData,
        }));

        setSubjectData(transformed);

      } else {
        throw new Error(data.message);
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error(error);
        alert(error.message);
      } else {
        console.error('Unknown error:', error);
        alert('An unexpected error occurred.');
      }
    }
  };

  return (
    <div className="p-5 space-y-4">
      <div className="flex w-full items-center space-x-2">
        <Input
          value={school}
          onChange={(e) => setSchool(e.target.value)}
          placeholder="Enter School Name"
        />
        <Button onClick={handleSubmit} className="text-black">
          Search
        </Button>
      </div>

      {subjectData.length > 0 && (
        <Table>
        <TableCaption>Band 6 predictions for {school}</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead >Subject</TableHead>
            {years.map((year) => (
                <TableHead key={year}>{year}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
        {subjectData.map((subject, index) => (
          <TableRow key={index}>
            <TableCell className="font-medium">{subject.subject}</TableCell>
            {years.map((year) => (
                <TableCell key={year}> {subject[year] ?? 0}</TableCell>
            ))}
          </TableRow>
        ))}
      </TableBody>
      </Table>
      )}

    </div>
  );
}

export default Band6;
