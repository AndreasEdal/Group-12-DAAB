using Avro;
using Avro.Specific;

namespace KafkaDocker;

public class Commit : ISpecificRecord


{
    public static Schema _SCHEMA = Avro.Schema.Parse(@"{""type"": ""record"",""name"": ""Commit"",""namespace"": ""ca.dataedu"",""fields"": [{""name"": ""commit"",""type"": [""null"", ""string""], ""default"": null}, { ""name"": ""message"",""type"": [""null"", ""string""],""default"": null }]}");
    public string commit;
    public string message;
    public virtual Schema Schema => _SCHEMA;

    public object Get(int fieldPos)
    {
        switch (fieldPos)
        {
            case 0: return this.commit;
            case 1: return this.message;
            default: throw new AvroRuntimeException("Bad index " + fieldPos + " in Get()");
        };
    }

    public void Put(int fieldPos, object fieldValue)
    {
        switch (fieldPos)
        {
            case 0: this.commit = (System.String)fieldValue; break;
            case 1: this.message = (System.String)fieldValue; break;
            default: throw new AvroRuntimeException("Bad index " + fieldPos + " in Put()");
        };
    }
    public override string ToString()
    {
        return $"Commit: {this.commit}, msg:'{this.message.Trim()}'";
    }
    
}