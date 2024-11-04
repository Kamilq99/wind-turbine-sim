let turbineOn = false;

function toggleTurbine() {
    turbineOn = !turbineOn;
    document.getElementById('turbineStatus').innerText = turbineOn ? 'ON' : 'OFF';

    // Dodawanie lub usuwanie animacji dla całej turbiny
    const turbine = document.getElementById('turbine');
    if (turbineOn) {
        turbine.classList.add('turbine-rotate');
    } else {
        turbine.classList.remove('turbine-rotate');
    }
}

function setSpeed() {
    const targetSpeed = document.getElementById('targetSpeed').value;
    document.getElementById('currentSpeed').innerText = targetSpeed;

    // Prędkość obrotu zależna od wartości
    const rotationDuration = 2000 / (targetSpeed / 100);  // Prędkość obrotu w milisekundach
    const turbine = document.getElementById('turbine');
    turbine.style.animationDuration = `${rotationDuration}ms`;
}