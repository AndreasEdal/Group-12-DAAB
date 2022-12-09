using System.Collections;
using System.Diagnostics;
using Newtonsoft.Json;
using Confluent.Kafka;


var config = new ProducerConfig
{
    BootstrapServers = "kafka:9092",
    CompressionType = CompressionType.Snappy,
    LingerMs = 5
};
using var producer = new ProducerBuilder<Null, string>(config).Build();
try
{
    using (StreamReader sr = new StreamReader("/App/content.json"))
    {
        while (!sr.EndOfStream)
        {
            string? json = await sr.ReadLineAsync();
            var result = await producer.ProduceAsync("content", new Message<Null, string> { Value = json }); 
        }
    }
}
catch (Exception e)
{
    Console.WriteLine(e.ToString());
}