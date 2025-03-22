import Form from "./components/Form";

function Header() {
  return (
    <header className="bg-green-600 text-white p-5 text-center text-2xl font-bold">
      Crop Prediction System
    </header>
  );
}

function AboutSection() {
  return (
    <section className="bg-yellow-300 p-8 text-center">
      <h2 className="text-2xl font-bold text-green-800">🌱 About Our System</h2>
      <p className="mt-4 text-green-700">
        Our Crop Prediction System uses advanced algorithms to suggest the best crops based on soil parameters and weather conditions.
        Enter the values for nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall to get accurate predictions.
      </p>
    </section>
  );
}

function Footer() {
  return (
    <footer className="bg-green-700 text-white text-center p-4 mt-10">
      © 2025 Crop Prediction. Made with ❤️ by Vasu Nandan.
    </footer>
  );
}

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <AboutSection />
      <main className="flex-grow flex items-center justify-center">
        <div className="bg-white shadow-lg rounded-xl p-8 max-w-md w-full">
          <Form />
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
