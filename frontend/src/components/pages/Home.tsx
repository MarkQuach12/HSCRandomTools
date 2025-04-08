import {
    Card,
  } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"

function Home() {
    return (
        <div className="p-5 space-y-4 ">
            <h2 className="text-5xl font-semibold">HSC Random Tools</h2>
            <p>A set of HSC tools including a scaled mark predictor and Band 6 school stats to help you understand your performance.</p>

            <Separator className="my-8" />

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 ">
                <Card className="p-4">
                    <h3 className ="text-xl font-semibold">Scaled Mark Predictor</h3>
                    <p>A tool that predicts NSW HSC student's scaled marks based on their raw scores for past years.</p>
                </Card>

                <Card className="p-4">
                    <h3 className ="text-xl font-semibold">Band 6 List</h3>
                    <p>Displays the number of Band 6 results for each subject at every school across previous HSC years.</p>
                </Card>

                <Card className="p-4">
                    <h3 className ="text-xl font-semibold">More Tools!</h3>
                    <p>Coming soon...</p>
                </Card>
            </div>

        </div>
    )
}


export default Home;