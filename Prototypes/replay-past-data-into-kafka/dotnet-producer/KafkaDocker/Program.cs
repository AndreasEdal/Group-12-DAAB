using Confluent.Kafka;

var config = new ProducerConfig
{
    BootstrapServers = "kafka:9092",
};

using var producer = new ProducerBuilder<Null, string>(config).Build();
var result = await producer.ProduceAsync("foobar", new Message<Null, string> {Value = "message"});
