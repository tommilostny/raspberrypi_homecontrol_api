using Newtonsoft.Json;
using System.Net;

namespace RpiHomeHub.BlazorWeb.Core.Models
{
    public class ResponseModel
    {
        public string Message { get; set; }

        [JsonIgnore]
        public HttpStatusCode Code { get; set; }
    }
}
