// ===============================
// CareerLens AI - Firebase Setup
// ===============================

import { initializeApp } from
    "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";

import {
    getFirestore
} from
    "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";


// ===============================
// Firebase Configuration
// ===============================

const firebaseConfig = {

    apiKey: "AIzaSyBIvOU66izJ01ep3240y022-jy6RSSB8gww",

    authDomain: "careerlens-ai-44bcb.firebaseapp.com",

    projectId: "careerlens-ai-44bcb",

    storageBucket: "careerlens-ai-44bcb.firebasestorage.app",

    messagingSenderId: "1053671693829",

    appId: "1:1053671693829:web:54beba1643f7b25125c66c",

    measurementId: "G-RT9CTEM4WB"

};


// ===============================
// Initialize Firebase
// ===============================

const app = initializeApp(firebaseConfig);


// ===============================
// Initialize Firestore
// ===============================

const db = getFirestore(app);


// ===============================
// Export Firestore
// ===============================

export { db };


console.log(
    "Firebase connected successfully!"
);