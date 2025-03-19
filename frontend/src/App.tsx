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
  const [predictedMark, setPredictedMark] = useState(null)
  const [band, setBand] = useState("Not Available")

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
          value='rawMark'
          onchange={(e) => setRawMark(e.target.value)}
        />
        <Button className='w-full mt-4' variant="outline">Predict Scaled Mark</Button>
        </CardContent>
        </Card>
      </div>
    </>
  )
}

export default App
