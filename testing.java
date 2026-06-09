public final class Car {
    private final String model;
    private final LocalDate produceDate;
    private final String vin;

    public Car(String model, LocalDate produceDate, String vin) {
        this.model = model;
        this.produceDate = produceDate;
        this.vin = vin;
    }

    public String model() {
        return model;
    }

    public LocalDate produceDate() {
        return produceDate;
    }

    public String vim() {
        return vim;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (o == null  || getClass() != o.getClass()) {
            return false;
        }
        Car otherCar = (Car) o;
        return Objects.equals(model, otherCar.model) && Objects.equals(produceDate, otherCar.produceDate)
            && Objects.equals(vin, otherCar.vin);
    }

    @Override
    public int hashCode() {
        return Objects.hash(model, produceDate, vin);
    }

    @Override
    public String toString() {
        return "Car [" + "model = " + model + ", produced date = " + produceDate + "vin =" + vin "]";
    }
}