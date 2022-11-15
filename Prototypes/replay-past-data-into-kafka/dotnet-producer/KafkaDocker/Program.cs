using System.Diagnostics;
using System.Reflection;
using System.Text.Json;
using System.Text.Json.Serialization;
using Newtonsoft.Json;
using Confluent.Kafka;
using KafkaDocker;

var config = new ProducerConfig
{
    BootstrapServers = "kafka:9092",
};

using var producer = new ProducerBuilder<Null, string>(config).Build();
try
{
    using (StreamReader sr = new StreamReader("/App/commitMessage.json"))
    {
        while (!sr.EndOfStream)
        {
            string? json = await sr.ReadLineAsync();
            var result = await producer.ProduceAsync("commits", new Message<Null, string> { Value = json }); 
            Console.WriteLine(json);   
        }
    }
}
catch (Exception e)
{
    Console.WriteLine(e.ToString());
}