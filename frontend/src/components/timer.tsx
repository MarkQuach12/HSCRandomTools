import { useState, useEffect } from 'react';

function Timer() {
    const updateTimer = () => {
        const now = new Date();
        const finalDate = new Date("October 16, 2025 09:50:00");

        const difference = finalDate.getTime() - now.getTime();
        const days = Math.floor(difference / (1000 * 3600 * 24));
        const hours = Math.floor((difference % (1000 * 3600 * 24)) / (1000 * 3600));
        const minutes = Math.floor((difference % (1000 * 3600)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        return {
          days: days,
          hours: hours,
          minutes: minutes,
          seconds: seconds
        }
    }

    const [timeLeft, setTimeLeft] = useState(updateTimer())

    useEffect(() => {
        const interval = setInterval(() => {
        const newTimeLeft = updateTimer();
        setTimeLeft(newTimeLeft);
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    return (
        <b className="!text-black !text-base">{timeLeft.days} d {timeLeft.hours} h {timeLeft.minutes} m {timeLeft.seconds} s left until English Paper 1</b>
    )
}

export default Timer;