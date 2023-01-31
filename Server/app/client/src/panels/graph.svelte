<a class="block md:w-full px-4 py-2 border-b border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-700 cursor-default">
    <div>
        <canvas id="temperatureChart"></canvas>
    </div>
</a>
<a class="block md:w-full px-4 py-2 border-b border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-700 cursor-default">
    <div>
        <canvas id="humidityChart"></canvas>
    </div>
</a>
<a class="block md:w-full px-4 py-2 border-b border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-700 cursor-default">
    <div>
        <canvas id="pressureChart"></canvas>
    </div>
</a>

<script>
    import { onMount } from 'svelte';
    import { Chart } from 'chart.js/auto';
    export let dataGet = {}
    
    console.log(dataGet)
    let dates = dataGet.map(a => a.create_time);
    let temperature = dataGet.map(a => a.temperature);
    let humidity = dataGet.map(a => a.humidity);
    let pressure = dataGet.map(a => a.pressure);
    console.log("test")
    Chart.defaults.backgroundColor = '#9BD0F5';
    Chart.defaults.borderColor = '#36A2EB';
    Chart.defaults.color = '#FFF';
    let data = function (data,title){
        return {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: title,
                    data: data,
                    fill: false,
                    borderColor: 'rgb(75, 192, 192)',
                    responsive: true, 
                    scaleFontColor: "#FFFFFF",
                    tension: 0.3
                }],
                grid: {
                    color: "white"
                },
                scales: {
                    x: {
                        ticks: {
                        color: "white"
                        }
                    },
                    y: {
                        ticks: {
                        color: "white"
                        }
                    }
                }
            }
        }
    }
    let chartTemp;
    let chartPress
    let chartHumid
    let mount = function(){

        chartTemp = new Chart(document.getElementById('temperatureChart').getContext('2d'), data(temperature, "Temperatura"));
        chartPress = new Chart(document.getElementById('pressureChart').getContext('2d'), data(pressure, "Ciśnienie"));
        chartHumid = new Chart(document.getElementById('humidityChart').getContext('2d'), data(humidity, "Wilgotność"));
        console.log("test")
    }
    onMount(mount)
</script>