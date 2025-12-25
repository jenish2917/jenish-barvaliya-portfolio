// JALA Academy - JavaScript Assignment

// Getting DOM elements
const contactForm = document.getElementById('contactForm');
const services = document.querySelectorAll('.service');
const navLinks = document.querySelectorAll('nav ul li a');

// Handle form submission
contactForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get the values from form
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // Check if all fields have values
    if(name && email && message) {
        alert(`Thanks ${name}! Your message was sent.`);
        contactForm.reset();
    } else {
        alert('Please fill all required fields.');
    }
});

// Add click events to service boxes
services.forEach((service, index) => {
    service.addEventListener('click', function() {
        alert(`You clicked: ${this.querySelector('h3').textContent}`);
    });
});

// Smooth scrolling for navigation
navLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        window.scrollTo({
            top: targetSection.offsetTop - 70,
            behavior: 'smooth'
        });
    });
});

// Add content after page loads
function addDynamicContent() {
    const homeSection = document.getElementById('home');
    const newParagraph = document.createElement('p');
    newParagraph.textContent = 'This paragraph was added with JavaScript!';
    newParagraph.style.backgroundColor = '#e8f4fd';
    newParagraph.style.padding = '1rem';
    newParagraph.style.borderRadius = '5px';
    newParagraph.style.marginTop = '1rem';
    newParagraph.style.borderLeft = '4px solid #667eea';
    
    homeSection.appendChild(newParagraph);
}

// Add the content after 2 seconds
window.addEventListener('load', function() {
    setTimeout(addDynamicContent, 2000);
});

// Change border color when user focuses on name field
document.getElementById('name').addEventListener('focus', function() {
    this.style.borderColor = '#667eea';
});

document.getElementById('name').addEventListener('blur', function() {
    this.style.borderColor = '#ddd';
});

// Check email format as user types
document.getElementById('email').addEventListener('input', function() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if(!emailRegex.test(this.value)) {
        this.style.backgroundColor = '#ffe6e6';
    } else {
        this.style.backgroundColor = 'white';
    }
});

// Create service element
function createServiceElement(title, description) {
    const serviceDiv = document.createElement('div');
    serviceDiv.className = 'service';
    
    const titleElement = document.createElement('h3');
    titleElement.textContent = title;
    
    const descElement = document.createElement('p');
    descElement.textContent = description;
    
    serviceDiv.appendChild(titleElement);
    serviceDiv.appendChild(descElement);
    
    return serviceDiv;
}

// List of services
const serviceList = [
    {title: "Cyber Security", description: "Security training program"},
    {title: "Data Science", description: "Analytics and machine learning"},
    {title: "Cloud", description: "AWS, Azure, Google Cloud training"}
];

// Add services to page
function addNewServices() {
    const container = document.querySelector('.services-container');
    
    serviceList.forEach(service => {
        const serviceElement = createServiceElement(service.title, service.description);
        container.appendChild(serviceElement);
    });
}

// Show current time in console
function updateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    console.log(`Time: ${timeString}`);
}

// Update time every second
setInterval(updateTime, 1000);

// Save user data to local storage
function saveUserData() {
    const userData = {
        name: document.getElementById('name').value || 'Guest',
        lastVisit: new Date().toISOString()
    };
    
    localStorage.setItem('jalaUserData', JSON.stringify(userData));
}

function loadUserData() {
    const userData = localStorage.getItem('jalaUserData');
    if(userData) {
        const parsedData = JSON.parse(userData);
        console.log('Welcome back,', parsedData.name);
        console.log('Last visit:', parsedData.lastVisit);
    }
}

// Save data when form is submitted
contactForm.addEventListener('submit', saveUserData);

// Load data when page loads
window.addEventListener('load', loadUserData);

// Array examples
const students = [
    {name: "Alice", grade: 85, course: "JavaScript"},
    {name: "Bob", grade: 92, course: "Python"},
    {name: "Charlie", grade: 78, course: "Java"}
];

// Find students with grade > 80
const highPerformers = students.filter(student => student.grade > 80);
console.log('Good students:', highPerformers);

// Get just the names
const studentNames = students.map(student => student.name);
console.log('Names:', studentNames);

// Calculate average grade
const averageGrade = students.reduce((sum, student) => sum + student.grade, 0) / students.length;
console.log(`Average grade: ${averageGrade.toFixed(2)}`);

// Handle clicks on service boxes
document.addEventListener('click', function(e) {
    if(e.target.classList.contains('service')) {
        e.target.style.transform = 'scale(1.05)';
        setTimeout(() => {
            e.target.style.transform = '';
        }, 300);
    }
});

// Promise example
function simulateAPICall() {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            const success = Math.random() > 0.3; // 70% chance of success
            if(success) {
                resolve({message: "Data loaded!", data: [1, 2, 3, 4, 5]});
            } else {
                reject({error: "Could not load data"});
            }
        }, 1000);
    });
}

// Using the promise
simulateAPICall()
    .then(response => {
        console.log(response.message);
        console.log("Data:", response.data);
    })
    .catch(error => {
        console.error("Error:", error.error);
    });

// Async/await example
async function fetchUserData() {
    try {
        const response = await simulateAPICall();
        console.log("Result:", response.message);
    } catch (error) {
        console.error("Error:", error.error);
    }
}

// Call the async function
fetchUserData();

// Simple class example
class Student {
    constructor(name, course) {
        this.name = name;
        this.course = course;
        this.enrollmentDate = new Date();
    }
    
    getInfo() {
        return `${this.name} is in ${this.course} since ${this.enrollmentDate.toDateString()}`;
    }
    
    updateCourse(newCourse) {
        this.course = newCourse;
        console.log(`${this.name} moved to ${newCourse}`);
    }
}

// Using the class
const student1 = new Student("John", "JavaScript");
console.log(student1.getInfo());
student1.updateCourse("Advanced JavaScript");

// Simple counter function
class Counter {
    constructor() {
        this.count = 0;
    }
    
    increment() {
        this.count++;
        return this.count;
    }
}

const counter = new Counter();
console.log("Count:", counter.increment());
console.log("Count:", counter.increment());
console.log("Count:", counter.increment());

// Final message
console.log("JavaScript assignment done!");