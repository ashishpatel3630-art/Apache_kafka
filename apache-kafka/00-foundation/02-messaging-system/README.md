# 02 - Messaging System 

Messaging system is a system that allows different applications, services, or components to communicate with each other by sending and receiving messages.

# Messaging System = One system sends information, another system receives and processes that information. 

# 1. Why Do We Need a Messaging System?

Imagine we have an e-commerce application.

A user places an order:

User
  │
  ▼
Order Service
  │
  ├──► Payment Service
  ├──► Inventory Service
  ├──► Notification Service
  └──► Analytics Service

Without a messaging system, the Order Service may directly call every service.

Order Service
    │
    ├── HTTP ──► Payment Service
    │
    ├── HTTP ──► Inventory Service
    │
    ├── HTTP ──► Notification Service
    │
    └── HTTP ──► Analytics Service

This creates strong coupling.

If the Notification Service is down, the Order Service may also be affected.

A messaging system changes the architecture:

                    ┌─────────────────┐
                    │  Payment        │
                    │  Service        │
                    └────────▲────────┘
                             │
                             │
┌──────────────┐       ┌─────┴─────┐
│ Order        │       │           │
│ Service      ├──────►│  Message  │
└──────────────┘       │   Broker  │
                       │           │
                       └─────┬─────┘
                             │
                 ┌───────────┼───────────┐
                 │           │           │
                 ▼           ▼           ▼
             Inventory   Notification  Analytics

Now the Order Service doesn't need to directly communicate with every consumer.


# 2. What is a Messages ?? 

A Messages is a piece of information transferred from one component to another . 

# 3. What Is Messaging?

A Messaging is the process of exchanging message between applications or services 

Example:

Producer
   │
   │ Message
   ▼
Messaging System
   │
   │ Message
   ▼
Consumer

Producer = producer creates/ sends the message 
Messaging system = The messaging system transport / or stores 
consumer = The consumer receives and processes the message.

# 4. Main Components of a Messaging System

Producer
   │
   ▼
Broker / Messaging System
   │
   ▼
Consumer

# 4.1 producer 

A Producer is an application or service that sends messages.

# 4.2 Consumer

A Consumer is an application or service  that receives and processess the messages .

# 4.3 Broker 

A Broker is the server that receives, stores, and serves messages.

In Kafka:

Producer
   │
   ▼
Kafka Broker
   │
   ▼
Consumer

A Kafka cluster normally contains multiple brokers.

# 5 Topic 
A Kafka topic is a logical category or stream to which producers write records and from which consumers read records. 

# Partition 

Kafka topic are divided into parts are called partition

Partition 0 ---------------- Order 101 Order 104 Order 107
Partition 1 ---------------- Order 102 Order 105 Order 108 
Partition 2 ---------------- Order 103 Order 106 Order 109

# OFFSET

Each record inside a Kafka partition has an offset.

# 6. Consumer Group

A consumer group is a group of consumers that cooperate to consume records from Kafka.