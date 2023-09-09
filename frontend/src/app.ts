import { fetchLocations, sendPredictionRequest } from './apiService.js';

document.getElementById('predict-form')?.addEventListener('submit', async (event: Event) => {
    event.preventDefault();

    const formElement = event.target as HTMLFormElement;
    const formData = new FormData(formElement);

    const requestPayload = {
        city: formData.get('city') as string,
        suburb: formData.get('suburb') as string,
        houseType: formData.get('house_type') as string,
        bedroomCount: Number(formData.get('bedroom_count')),
        bathroomCount: Number(formData.get('bathroom_count')),
        priceIncludesBills: (formData.get('price_includes_bills') as string) === 'on',
        roomsAvailable: Number(formData.get('rooms_available'))
    };

    const resultElement = document.getElementById('result') as HTMLElement;
    const { prediction, error } = await sendPredictionRequest(requestPayload);
    if (prediction) {
        resultElement.innerText = `Predicted Value: ${prediction} per room`;
    } else {
        resultElement.innerText = error || 'Error predicting value';
    }
});


document.addEventListener("DOMContentLoaded", function () {
    fetchLocations()
        .then(data => {
            populateDataList('cities', data.cities);
            populateDataList('suburbs', data.suburbs);
            populateDropdown('house_type', data.house_types);
        })
        .catch(error => {
            console.error('There was an error fetching data:', error);
        });
});


function populateDropdown(id: string, items: string[]) {
    const dropdown = document.getElementById(id) as HTMLSelectElement;
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        dropdown.appendChild(option);
    });
}

function populateDataList(id: string, items: string[]) {
    const dataList = document.getElementById(id) as HTMLDataListElement;
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        dataList.appendChild(option);
    });
}
