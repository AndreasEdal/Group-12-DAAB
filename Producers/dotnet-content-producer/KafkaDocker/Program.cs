using System.Collections;
using System.Diagnostics;
using Newtonsoft.Json;
using Confluent.Kafka;


var bootstrapServers = "kafka:9092";
Console.WriteLine($"Using '{bootstrapServers}' as bootstrap server");
Random rnd = new Random();
var config = new ProducerConfig
{
    BootstrapServers = bootstrapServers,
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
            //Console.WriteLine(json);
            //Thread.Sleep(rnd.Next(0.1,1));
        }
    }
}
catch (Exception e)
{
    Console.WriteLine(e.ToString());
    Environment.Exit(-1);
    throw;
}