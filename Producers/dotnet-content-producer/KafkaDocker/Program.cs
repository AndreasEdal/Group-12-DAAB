using System.Collections;
using System.Diagnostics;
using Newtonsoft.Json;
using Confluent.Kafka;
using Confluent.SchemaRegistry;
using Confluent.SchemaRegistry.Serdes;
using KafkaDocker;
using SolTechnology.Avro;


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
var avroSerializerConfig = new AvroSerializerConfig
{
    // optional Avro serializer properties:
    BufferBytes = 100,
};

var schemaRegistryConfig = new SchemaRegistryConfig
{
    // Note: you can specify more than one schema registry url using the
    // schema.registry.url property for redundancy (comma separated list). 
    // The property name is not plural to follow the convention set by
    // the Java implementation.
    Url = "http://schema-registry:6969"
};

using (var schemaRegistry = new CachedSchemaRegistryClient(schemaRegistryConfig))
using (var producer2 =
       new ProducerBuilder<Null, byte[]>(config)
            .SetValueSerializer(new AvroSerializer<byte[]>(schemaRegistry, avroSerializerConfig))
           .Build())
{
    using (var sr1 = new StreamReader("/App/content.json"))
    {
        while (!sr1.EndOfStream)
        {
            var json = await sr1.ReadLineAsync();
            //  Console.WriteLine(avroObject);
            //Console.WriteLine(json);
            var content = JsonConvert.DeserializeObject<Content>(json);
            // Console.WriteLine(dynamicObject);
            var avroObject = AvroConvert.Serialize(content, CodecType.Snappy);
            //Commit deserializedObject = AvroConvert.Deserialize(avroObject, typeof(Commit));
            //var result = await producer2.ProduceAsync("commits_avro", new Message<Null, Commit> { Value = dynamicObject ?? new Commit() });
            var result = await producer2.ProduceAsync("content_avro", new Message<Null, byte[]> { Value = avroObject });
            
        }
    }
}