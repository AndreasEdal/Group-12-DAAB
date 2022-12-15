﻿using System.Collections;
using System.Diagnostics;
using Newtonsoft.Json;
using Confluent.Kafka;

var bootstrapServers = "kafka:9092";
Console.WriteLine("Language Producer Running...");
//Console.WriteLine($"Using '{bootstrapServers}' as bootstrap server");
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
    using (StreamReader sr = new StreamReader("/App/languages.json"))
    {
        while (!sr.EndOfStream)
        {
            string? json = await sr.ReadLineAsync();
            var result = await producer.ProduceAsync("languages", new Message<Null, string> { Value = json }); 
            Thread.Sleep(rnd.Next(100,1000));
        }
    }
}
catch (Exception e)
{
    Console.WriteLine(e.ToString());
    Environment.Exit(-1);
    throw;
}