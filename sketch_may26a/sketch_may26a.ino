// Definindo os pinos dos sensores reflexivos
const int sensor1 = 4;
const int sensor2 = 5;
const int sensor3 = 6;

// Definindo os pinos do sensor de cor 1
const int S0_1 = 7;
const int S1_1 = 8;
const int S2_1 = 9;
const int S3_1 = 10;
const int outPin_1 = 11;

// Definindo os pinos do sensor de cor 2
const int S0_2 = 12;
const int S1_2 = 13;
const int S2_2 = 14; // Pode ser qualquer pino digital disponível
const int S3_2 = 15; // Pode ser qualquer pino digital disponível
const int outPin_2 = 16; // Pode ser qualquer pino digital disponível

// Função para configurar os sensores de cor
void setupColorSensor(int S0, int S1, int S2, int S3, int outPin) {
    pinMode(S0, OUTPUT);
    pinMode(S1, OUTPUT);
    pinMode(S2, OUTPUT);
    pinMode(S3, OUTPUT);
    pinMode(outPin, INPUT);
    
    // Configura a escala de frequência do sensor (100% de escala)
    digitalWrite(S0, HIGH);
    digitalWrite(S1, LOW);
}

// Função para ler os valores de cor
void readColor(int S2, int S3, int outPin, int &red, int &green, int &blue) {
    // Lê a cor vermelha
    digitalWrite(S2, LOW);
    digitalWrite(S3, LOW);
    red = pulseIn(outPin, LOW);

    // Lê a cor verde
    digitalWrite(S2, HIGH);
    digitalWrite(S3, HIGH);
    green = pulseIn(outPin, LOW);

    // Lê a cor azul
    digitalWrite(S2, LOW);
    digitalWrite(S3, HIGH);
    blue = pulseIn(outPin, LOW);
}

void setup() {
    Serial.begin(115200);
    pinMode(sensor1, INPUT);
    pinMode(sensor2, INPUT);
    pinMode(sensor3, INPUT);

    // Configura os sensores de cor
    setupColorSensor(S0_1, S1_1, S2_1, S3_1, outPin_1);
    setupColorSensor(S0_2, S1_2, S2_2, S3_2, outPin_2);
}

void loop() {
    int Valor1 = digitalRead(sensor1);
    int Valor2 = digitalRead(sensor2);
    int Valor3 = digitalRead(sensor3);

    // Variáveis para armazenar as leituras de cor dos sensores de cor
    int red1, green1, blue1;
    int red2, green2, blue2;

    // Lê as cores do sensor de cor 1
    readColor(S2_1, S3_1, outPin_1, red1, green1, blue1);

    // Lê as cores do sensor de cor 2
    readColor(S2_2, S3_2, outPin_2, red2, green2, blue2);

    // Verifica os sensores reflexivos e envia dados ao EV3
    if (Valor1 == 0 && Valor2 == 0 && Valor3 == 0) {
        Serial.println(1); // Enviar 1 se todos os valores forem 0
    } else if (Valor1 == 0 && Valor2 == 0 && Valor3 != 0) {
        Serial.println(2); // Enviar 2 se Valor1 e Valor2 forem 0 e Valor3 for diferente de 0
    } else if (Valor1 == 0 && Valor2 != 0 && Valor3 == 0) {
        Serial.println(3); // Enviar 3 se Valor1 for 0, Valor2 for diferente de 0 e Valor3 for 0
    }

    // Verifica se algum dos sensores de cor detectou verde
    if ((green1 < red1 && green1 < blue1) || (green2 < red2 && green2 < blue2)) {
        Serial.println(5); // Enviar 5 se a cor verde for detectada por qualquer sensor
    } else if(green2 < red2 && green2 < blue2){
        Serial.println(6);
    } else if(green1 < red1 && green1 < blue1){
        Serial.println(7);
    }

    delay(1000); // Espera 1 segundo antes de ler novamente
}
