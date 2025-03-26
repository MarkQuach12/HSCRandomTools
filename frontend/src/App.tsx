import { useState } from 'react'
import './App.css'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"


function App() {
  const [subject, setSubject] = useState("")
  const [rawMark, setRawMark] = useState("")
  const [predictions, setPredictions] = useState([])

  const handleSubmit = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_REACT_APP_BACKEND_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          subject: subject,
          rawMark: parseFloat(rawMark),
        }),
      })

      const data = await response.json()

      if (response.ok) {
        setPredictions(data.predictions)
      } else {
        throw new Error(data.message)
      }
    } catch (error) {
      console.error(error)
      alert(error.message)
    }
  }

  return (
    <>
      <div className='flex flex-col items-center p-6'>
      <Card className='w-full max-w-3xl min-h-[300px] p-8'>
        <CardHeader>
          <CardTitle className="text-2xl font-bold">HSC Scaled Mark Predictor</CardTitle>
        </CardHeader>
        <CardContent>
        <Input
            placeholder='Enter Subject'
            className='mt-4'
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
          />
        <Input
          type='number'
          placeholder='Enter Raw Mark'
          className='mt-2'
          value={rawMark}
          onChange={(e) => setRawMark(e.target.value)}
          min={0}
          max={100}
        />
        <Button className='w-full mt-4' variant="outline" onClick={handleSubmit}>Predict Scaled Mark</Button>

        {predictions.length > 0 && (
          <div className = 'mt-6'>
            <h3 classname = 'text-lg font-semibold mb-2'> Predictions</h3>
            <ul className = 'space-y-1'>
              {predictions.map((item, index) => (
                <li key='index'>
                  {item.year} : <strong>{item.predicted_mark}</strong>
                </li>
              ))}
            </ul>
          </div>
        )}
        </CardContent>
        </Card>
      </div>
    </>
  )
}

export default App
