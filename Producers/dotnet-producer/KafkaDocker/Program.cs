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
    using (StreamReader sr = new StreamReader("/App/commitMessage.json"))
    {
        while (!sr.EndOfStream)
        {
            string? json = await sr.ReadLineAsync();
            //Console.WriteLine(json);
            var result = await producer.ProduceAsync("commits_json", new Message<Null, string> { Value = json }); 
            //Console.WriteLine(json);   
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

// Without serializer (manual)
using (var schemaRegistry = new CachedSchemaRegistryClient(schemaRegistryConfig))
using (var producer2 =
       new ProducerBuilder<Null, byte[]>(config)
         //  .SetValueSerializer(new AvroSerializer<byte[]>(schemaRegistry, avroSerializerConfig))
           .Build())
{
    using (var sr1 = new StreamReader("/App/commitMessage.json"))
    {
        while (!sr1.EndOfStream)
        {
            var json = await sr1.ReadLineAsync();
            //  Console.WriteLine(avroObject);
            
            var dynamicObject = JsonConvert.DeserializeObject<Commit>(json);
            dynamicObject?.commit.Trim();
            dynamicObject?.message.Trim();
           // Console.WriteLine(dynamicObject);
            var avroObject = AvroConvert.Serialize(dynamicObject, CodecType.Snappy);
            //Commit deserializedObject = AvroConvert.Deserialize(avroObject, typeof(Commit));
            //var result = await producer2.ProduceAsync("commits_avro", new Message<Null, Commit> { Value = dynamicObject ?? new Commit() });
            var result = await producer2.ProduceAsync("commit", new Message<Null, byte[]> { Value = avroObject });
            
        }
    }
}

// With serializer (automatic)
/*
using (var schemaRegistry = new CachedSchemaRegistryClient(schemaRegistryConfig))
using (var producer2 =
       new ProducerBuilder<Null, Commit>(config)
           .SetValueSerializer(new AvroSerializer<Commit>(schemaRegistry, avroSerializerConfig))
           .Build())
{
    using (var sr1 = new StreamReader("/App/commitMessage.json"))
    {
        while (!sr1.EndOfStream)
        {
            var json = await sr1.ReadLineAsync();
            //  Console.WriteLine(avroObject);
            
            var commit = JsonConvert.DeserializeObject<Commit>(json);
            commit?.commit.Trim();
            commit?.message.Trim();
            Console.WriteLine(commit);
            //byte[] avroObject = AvroConvert.Serialize(commit, CodecType.Snappy);
            //Commit deserializedObject = AvroConvert.Deserialize(avroObject, typeof(Commit));
            //var result = await producer2.ProduceAsync("commits_avro", new Message<Null, Commit> { Value = dynamicObject ?? new Commit() });
            var result = await producer2.ProduceAsync("avro_topic_wrong", new Message<Null, Commit> { Value = commit ?? new Commit() });
            
        }
    }
}
*/



