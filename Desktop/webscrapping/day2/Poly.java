class Animal {
    public void makesound() {
        System.out.println("some generic animal sound");

    }

    public static void eat() {
        System.out.println("Animal is eating");

    }


}

class Dog extends Animal {
    @Override
    public void makesound() {
        System.out.println("Dogs bark Woof Woof");
    }

    public static void eat() {
        System.out.println("Dog is eating");
    }
}

public class Poly {
    public static void main(String[] args){
        Animal genericAnimal = new Animal();
        Dog myDog = new Dog();
        
        Animal.eat();
        Dog.eat();

        Animal polymorphicAnimal = new Dog();

        genericAnimal.makesound();

        myDog.makesound();
        polymorphicAnimal.makesound();
    }
}