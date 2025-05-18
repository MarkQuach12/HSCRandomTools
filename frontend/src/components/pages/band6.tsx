import { useState, useEffect } from 'react';
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
import { toast } from 'react-toastify';

function Band6() {
    const [school, setSchool] = useState('');
    const [subjectData, setSubjectData] = useState<any[]>([]);
    const [years, setYears] = useState<string[]>([]);
    const [allSchools, setAllSchools] = useState<string[]>([])
    const [filteredSchools, setFilteredSchools] = useState<string[]>([])
    const [showDropdown, setShowDropdown] = useState(false)

    useEffect(() => {
        const fetchSchools = async () => {
            const response = await fetch(`${import.meta.env.VITE_REACT_APP_BACKEND_URL}/band6/schools`);
            console.log(response)
            const data = await response.json();
            setAllSchools(data.schools);
            console.log("Fetched schools:", data.schools);
        }
        fetchSchools();
    }, [])

    const handleSelectSchool = (selectedSchool: string) => {
        setSchool(selectedSchool);
        setFilteredSchools([]);
        setShowDropdown(false);
    }

    const showToastMessage = (errorMessage: string) => {
        toast.error(errorMessage, {
            position: "bottom-right",
            autoClose: 4000,
            hideProgressBar: false,
            theme: "colored",
        });
    }

    const handleSubmit = async () => {
        if (school.trim() === '') {
            showToastMessage("Please enter a school name");
            return;
        }

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
            showToastMessage(error.message || "Please enter a valid school name");
        } else {
            console.error('Unknown error:', error);
            showToastMessage("An unknown error has occurred");
        }
        }
    };

    return (
        <div className="p-5 space-y-4">
        <h2 className="text-3xl font-semibold">Band 6 List</h2>

        <div className="flex w-full items-center space-x-2">
            <form
                onSubmit={(e) => {
                e.preventDefault();
                handleSubmit();
                }}
            className="flex w-full items-center space-x-2">
            <div className="relative w-full">
            <Input
                value={school}
                onChange={(e) => {
                    const input = e.target.value;
                    setSchool(input);
                    const filtered = allSchools.filter((s) =>
                        s.toLowerCase().startsWith(input.toLowerCase())
                    );
                    setFilteredSchools(filtered);
                    setShowDropdown(input.length > 0 && filtered.length > 0);
                }}
                placeholder="Enter School Name"
            />
            {showDropdown && (
                <ul className="absolute z-50 bg-white border rounded w-full max-h-60 overflow-auto shadow">
                {filteredSchools.map((s, index) => (
                    <li
                        key={index}
                        onClick={() => handleSelectSchool(s)}
                        className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                    >
                    {s}
                    </li>
                ))}
                </ul>
            )}
            </div>

        <Button type="submit" className="text-black">
            Search
        </Button>
        </form>

        </div>

        {subjectData.length > 0 && (
            <Table>
            <TableCaption>Band 6 predictions for {school}</TableCaption>
            <TableHeader>
            <TableRow>
                <TableHead >Subject</TableHead>
                {years.map((year, index) => (
                    <TableHead key={year} className={index === 0 ? 'bg-gray-100 font-bold' : ''}>{year}</TableHead>
                ))}
            </TableRow>
            </TableHeader>
            <TableBody>
            {subjectData.map((subject, index) => (
            <TableRow key={index}>
                <TableCell className="font-medium">{subject.subject}</TableCell>
                {years.map((year, index) => (
                    <TableCell key={year} className={index === 0 ? 'bg-gray-100 font-bold' : ''}> {subject[year] ?? 0}</TableCell>
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
