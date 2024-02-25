import { CONFIG } from './config.js';

export const fetchLocations = async () => {
    try {
        const response = await fetch(`${CONFIG.BASE_URL}/get-locations`);
        return await response.json();
    } catch (error) {
        console.error('Failed to fetch locations:', error);
        throw error;
    }
};


export async function fetchSuburbs(city: string): Promise<string[]> {
    const response = await fetch(`/get-suburbs?city=${city}`);
    if (response.ok) {
        const data = await response.json();
        return data.suburbs;
    } else {
        throw new Error('Failed to fetch suburbs');
    }
}


export async function sendPredictionRequest(requestPayload: {
    city: string;
    suburb: string;
    houseType: string;
    bedroomCount: number;
    bathroomCount: number;
    priceIncludesBills: boolean;
    roomsAvailable: number;
}): Promise<{ prediction?: number; error?: string }> {

    try {
        const response = await fetch(`${CONFIG.BASE_URL}/predict`, {
            method: 'POST',
            body: JSON.stringify(requestPayload),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            return { prediction: data.prediction };
        } else {
            return { error: 'Error predicting value' };
        }
    } catch (error) {
        console.error('There was an error sending the request', error);
        return { error: 'Failed to send prediction request' };
    }
}
